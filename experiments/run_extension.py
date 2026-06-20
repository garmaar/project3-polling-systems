import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.config import SimulationConfig
from src.simulation import PollingSimulation
from src.metrics import packets_to_dataframe


def jain_fairness(values):
    values = list(values)
    numerator = sum(values) ** 2
    denominator = len(values) * sum(v ** 2 for v in values)
    return numerator / denominator


def run_extension_scenario(discipline, seed):
    M = 10
    T = 3.0
    h = 0.8
    rho = 0.6

    hot_station = 0
    hot_factor = 2

    total_lambda = rho / T

    # We want:
    # lambda_hot = hot_factor * lambda_normal
    # lambda_hot + 9 * lambda_normal = total_lambda
    lambda_normal = total_lambda / (hot_factor + (M - 1))
    lambda_hot = hot_factor * lambda_normal

    arrival_rates = [
        lambda_hot if i == hot_station else lambda_normal
        for i in range(M)
    ]

    config = SimulationConfig(
        num_stations=M,
        total_arrival_rate=total_lambda,
        service_time=T,
        switch_time=h,
        discipline=discipline,
        limited_k=1,
        simulation_time=150_000.0,
        warmup_time=20_000.0,
        random_seed=seed,
    )

    simulation = PollingSimulation(config)

    # Override symmetric arrival rates with asymmetric ones
    for station, rate in zip(simulation.stations, arrival_rates):
        station.arrival_rate = rate

    packets = simulation.run()
    df = packets_to_dataframe(packets, config)

    per_station = (
        df.groupby("station_id")["waiting_time"]
        .mean()
        .reset_index()
    )

    per_station["discipline"] = discipline
    per_station["seed"] = seed
    per_station["arrival_rate"] = per_station["station_id"].map(
        lambda i: arrival_rates[int(i)]
    )
    per_station["is_hot_station"] = per_station["station_id"] == hot_station

    waiting_values = per_station["waiting_time"].values

    fairness = {
        "discipline": discipline,
        "seed": seed,
        "hot_station_waiting_time": per_station.loc[
            per_station["is_hot_station"], "waiting_time"
        ].iloc[0],
        "normal_mean_waiting_time": per_station.loc[
            ~per_station["is_hot_station"], "waiting_time"
        ].mean(),
        "max_min_ratio": per_station["waiting_time"].max()
        / per_station["waiting_time"].min(),
        "jain_fairness_index": jain_fairness(waiting_values),
    }

    return per_station, fairness


def main():
    output_dir = PROJECT_ROOT / "outputs" / "tables"
    output_dir.mkdir(parents=True, exist_ok=True)

    all_per_station = []
    all_fairness = []

    for discipline in ["exhaustive", "limited"]:
        for seed in [1, 2, 3]:
            per_station, fairness = run_extension_scenario(discipline, seed)
            all_per_station.append(per_station)
            all_fairness.append(fairness)

            print(
                f"OK | {discipline} | seed={seed} | "
                f"hot W={fairness['hot_station_waiting_time']:.4f} | "
                f"normal W={fairness['normal_mean_waiting_time']:.4f}"
            )

    per_station_df = pd.concat(all_per_station, ignore_index=True)
    fairness_df = pd.DataFrame(all_fairness)

    per_station_path = output_dir / "extension_per_station.csv"
    fairness_path = output_dir / "extension_fairness.csv"

    per_station_df.to_csv(per_station_path, index=False)
    fairness_df.to_csv(fairness_path, index=False)

    print()
    print(f"Saved per-station results to: {per_station_path}")
    print(f"Saved fairness results to: {fairness_path}")


if __name__ == "__main__":
    main()