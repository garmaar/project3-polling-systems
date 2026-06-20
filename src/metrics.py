import pandas as pd
from src.packet import Packet
from src.config import SimulationConfig


def packets_to_dataframe(
    packets: list[Packet],
    config: SimulationConfig,
) -> pd.DataFrame:
    rows = []

    for p in packets:
        if p.service_start_time is None or p.departure_time is None:
            continue

        if p.arrival_time < config.warmup_time:
            continue

        rows.append(
            {
                "packet_id": p.packet_id,
                "station_id": p.station_id,
                "arrival_time": p.arrival_time,
                "service_start_time": p.service_start_time,
                "departure_time": p.departure_time,
                "waiting_time": p.waiting_time,
                "sojourn_time": p.departure_time - p.arrival_time,
            }
        )

    return pd.DataFrame(rows)


def summarize_results(df: pd.DataFrame) -> dict:
    if df.empty:
        raise ValueError("No packets available after warm-up.")

    per_station = (
        df.groupby("station_id")["waiting_time"]
        .mean()
        .to_dict()
    )

    return {
        "num_packets": len(df),
        "mean_waiting_time": df["waiting_time"].mean(),
        "mean_sojourn_time": df["sojourn_time"].mean(),
        "per_station_waiting_time": per_station,
    }