import sys
from pathlib import Path

import pandas as pd

# Allow imports from project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.config import SimulationConfig
from src.simulation import PollingSimulation
from src.metrics import packets_to_dataframe, summarize_results
from src.theory import theoretical_waiting_time


def run_single_scenario(
    discipline: str,
    M: int,
    rho: float,
    T: float,
    h: float,
    k: int,
    sim_time: float,
    warmup: float,
    seed: int,
) -> dict:
    config = SimulationConfig(
        num_stations=M,
        service_time=T,
        switch_time=h,
        total_arrival_rate=rho / T,
        discipline=discipline,
        limited_k=k,
        simulation_time=sim_time,
        warmup_time=warmup,
        random_seed=seed,
    )

    simulation = PollingSimulation(config)
    packets = simulation.run()

    df = packets_to_dataframe(packets, config)
    summary = summarize_results(df)

    sim_w = summary["mean_waiting_time"]
    theory_w = theoretical_waiting_time(config)

    return {
        "discipline": discipline,
        "M": M,
        "rho": rho,
        "T": T,
        "h": h,
        "k": k,
        "seed": seed,
        "num_packets": summary["num_packets"],
        "simulation_EW": sim_w,
        "theoretical_EW": theory_w,
        "absolute_error": abs(sim_w - theory_w),
        "relative_error": abs(sim_w - theory_w) / theory_w,
    }


def main() -> None:
    output_dir = PROJECT_ROOT / "outputs" / "tables"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []

    disciplines = ["exhaustive", "limited"]
    rho_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    M_values = [5, 10, 20]
    seeds = [1, 2, 3]

    T = 3.0
    h = 0.8
    k = 1
    sim_time = 100_000.0
    warmup = 10_000.0

    for discipline in disciplines:
        for M in M_values:
            for rho in rho_values:
                for seed in seeds:
                    try:
                        result = run_single_scenario(
                            discipline=discipline,
                            M=M,
                            rho=rho,
                            T=T,
                            h=h,
                            k=k,
                            sim_time=sim_time,
                            warmup=warmup,
                            seed=seed,
                        )

                        results.append(result)

                        print(
                            f"OK | {discipline} | M={M} | rho={rho} | "
                            f"seed={seed} | rel_error={result['relative_error']:.2%}"
                        )

                    except ValueError as error:
                        print(
                            f"SKIP | {discipline} | M={M} | rho={rho} | "
                            f"seed={seed} | reason={error}"
                        )

    results_df = pd.DataFrame(results)

    output_path = output_dir / "experiment_results.csv"
    results_df.to_csv(output_path, index=False)

    print()
    print(f"Saved results to: {output_path}")


if __name__ == "__main__":
    main()