from dataclasses import dataclass
from typing import Literal


Discipline = Literal["exhaustive", "limited"]


@dataclass(frozen=True)
class SimulationConfig:
    num_stations: int = 10
    total_arrival_rate: float = 0.7 / 3.0   # lambda = rho / T
    service_time: float = 3.0               # T
    switch_time: float = 0.8                # h
    discipline: Discipline = "exhaustive"
    limited_k: int = 1
    simulation_time: float = 100_000.0
    warmup_time: float = 10_000.0
    random_seed: int = 42

    @property
    def arrival_rate_per_station(self) -> float:
        return self.total_arrival_rate / self.num_stations

    @property
    def load(self) -> float:
        return self.total_arrival_rate * self.service_time