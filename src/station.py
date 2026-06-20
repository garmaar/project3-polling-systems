from collections import deque
from src.packet import Packet


class Station:
    def __init__(self, station_id: int, arrival_rate: float):
        self.station_id = station_id
        self.arrival_rate = arrival_rate
        self.queue: deque[Packet] = deque()

    def enqueue(self, packet: Packet) -> None:
        self.queue.append(packet)

    def dequeue(self) -> Packet:
        return self.queue.popleft()

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def __len__(self) -> int:
        return len(self.queue)