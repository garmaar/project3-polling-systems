import simpy
from src.station import Station
from src.packet import Packet


def serve_packet(
    env: simpy.Environment,
    station: Station,
    service_time: float,
    packet_log: list[Packet],
) -> simpy.events.Event:
    packet = station.dequeue()
    packet.service_start_time = env.now

    yield env.timeout(service_time)

    packet.departure_time = env.now
    packet_log.append(packet)


def exhaustive_service(
    env: simpy.Environment,
    station: Station,
    service_time: float,
    packet_log: list[Packet],
):
    while not station.is_empty():
        yield from serve_packet(env, station, service_time, packet_log)


def limited_service(
    env: simpy.Environment,
    station: Station,
    service_time: float,
    packet_log: list[Packet],
    k: int,
):
    served_count = 0

    while not station.is_empty() and served_count < k:
        yield from serve_packet(env, station, service_time, packet_log)
        served_count += 1