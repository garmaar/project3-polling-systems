import itertools
import numpy as np
import simpy

from src.config import SimulationConfig
from src.packet import Packet
from src.station import Station
from src.disciplines import exhaustive_service, limited_service


class PollingSimulation:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.env = simpy.Environment()
        self.rng = np.random.default_rng(config.random_seed)

        self.packet_id_counter = itertools.count()

        self.stations = [
            Station(
                station_id=i,
                arrival_rate=config.arrival_rate_per_station,
            )
            for i in range(config.num_stations)
        ]

        self.packet_log: list[Packet] = []

    def arrival_process(self, station: Station):
        while True:
            interarrival_time = self.rng.exponential(
                1.0 / station.arrival_rate
            )
            yield self.env.timeout(interarrival_time)

            packet = Packet(
                packet_id=next(self.packet_id_counter),
                station_id=station.station_id,
                arrival_time=self.env.now,
            )

            station.enqueue(packet)

    def polling_server(self):
        i = 0

        while True:
            station = self.stations[i]

            if self.config.discipline == "exhaustive":
                yield from exhaustive_service(
                    env=self.env,
                    station=station,
                    service_time=self.config.service_time,
                    packet_log=self.packet_log,
                )

            elif self.config.discipline == "limited":
                yield from limited_service(
                    env=self.env,
                    station=station,
                    service_time=self.config.service_time,
                    packet_log=self.packet_log,
                    k=self.config.limited_k,
                )

            else:
                raise ValueError(f"Unknown discipline: {self.config.discipline}")

            yield self.env.timeout(self.config.switch_time)

            i = (i + 1) % self.config.num_stations

    def run(self) -> list[Packet]:
        for station in self.stations:
            self.env.process(self.arrival_process(station))

        self.env.process(self.polling_server())

        self.env.run(until=self.config.simulation_time)

        return self.packet_log