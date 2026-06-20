import argparse

from src.config import SimulationConfig
from src.simulation import PollingSimulation
from src.metrics import packets_to_dataframe, summarize_results
from src.theory import theoretical_waiting_time


DISCIPLINES = {
    "1": "exhaustive",
    "2": "limited",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Polling system simulator")

    parser.add_argument(
        "discipline",
        choices=["1", "2"],
        help="1 = exhaustive, 2 = limited / round-robin",
    )

    parser.add_argument("--M", type=int, default=10)
    parser.add_argument("--rho", type=float, default=0.7)
    parser.add_argument("--T", type=float, default=3.0)
    parser.add_argument("--h", type=float, default=0.8)
    parser.add_argument("--k", type=int, default=1)
    parser.add_argument("--sim-time", type=float, default=100_000.0)
    parser.add_argument("--warmup", type=float, default=10_000.0)
    parser.add_argument("--seed", type=int, default=42)

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    discipline = DISCIPLINES[args.discipline]

    config = SimulationConfig(
        num_stations=args.M,
        service_time=args.T,
        switch_time=args.h,
        total_arrival_rate=args.rho / args.T,
        discipline=discipline,
        limited_k=args.k,
        simulation_time=args.sim_time,
        warmup_time=args.warmup,
        random_seed=args.seed,
    )

    simulation = PollingSimulation(config)
    packets = simulation.run()

    df = packets_to_dataframe(packets, config)
    summary = summarize_results(df)

    theory_w = theoretical_waiting_time(config)
    sim_w = summary["mean_waiting_time"]

    print("=== POLLING SIMULATION RESULT ===")
    print(f"Discipline: {config.discipline}")
    print(f"M: {config.num_stations}")
    print(f"T: {config.service_time}")
    print(f"h: {config.switch_time}")
    print(f"k: {config.limited_k}")
    print(f"rho: {config.load:.4f}")
    print(f"lambda: {config.total_arrival_rate:.6f}")
    print(f"Packets after warm-up: {summary['num_packets']}")
    print()
    print(f"Simulation E[W]: {sim_w:.4f}")
    print(f"Theoretical E[W]: {theory_w:.4f}")
    print(f"Absolute error: {abs(sim_w - theory_w):.4f}")
    print(f"Relative error: {abs(sim_w - theory_w) / theory_w:.2%}")
    print()
    print("Per-station waiting time:")
    for station_id, waiting_time in summary["per_station_waiting_time"].items():
        print(f"  Station {station_id}: {waiting_time:.4f}")


if __name__ == "__main__":
    main()