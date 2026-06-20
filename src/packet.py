from dataclasses import dataclass


@dataclass
class Packet:
    packet_id: int
    station_id: int
    arrival_time: float
    service_start_time: float | None = None
    departure_time: float | None = None

    @property
    def waiting_time(self) -> float:
        if self.service_start_time is None:
            raise ValueError("Packet has not started service.")
        return self.service_start_time - self.arrival_time