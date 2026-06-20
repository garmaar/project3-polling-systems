import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


def plot_waiting_time_vs_rho(df: pd.DataFrame, output_dir: Path) -> None:
    for discipline in df["discipline"].unique():
        subset = df[df["discipline"] == discipline]

        plt.figure()

        for M in sorted(subset["M"].unique()):
            data = subset[subset["M"] == M].sort_values("rho")

            plt.plot(
                data["rho"],
                data["mean_simulation_EW"],
                marker="o",
                label=f"Simulation M={M}",
            )

            plt.plot(
                data["rho"],
                data["mean_theoretical_EW"],
                linestyle="--",
                label=f"Theory M={M}",
            )

        plt.xlabel("Traffic load ρ")
        plt.ylabel("Average waiting time E[W]")
        plt.title(f"Waiting time vs traffic load — {discipline}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        output_path = output_dir / f"waiting_time_vs_rho_{discipline}.png"
        plt.savefig(output_path, dpi=300)
        plt.close()


def plot_relative_error_vs_rho(df: pd.DataFrame, output_dir: Path) -> None:
    plt.figure()

    for discipline in df["discipline"].unique():
        subset = df[df["discipline"] == discipline]

        for M in sorted(subset["M"].unique()):
            data = subset[subset["M"] == M].sort_values("rho")

            plt.plot(
                data["rho"],
                100 * data["mean_relative_error"],
                marker="o",
                label=f"{discipline}, M={M}",
            )

    plt.xlabel("Traffic load ρ")
    plt.ylabel("Mean relative error [%]")
    plt.title("Simulation-theory relative error")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path = output_dir / "relative_error_vs_rho.png"
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_waiting_time_vs_M(df: pd.DataFrame, output_dir: Path) -> None:
    plt.figure()

    selected_rhos = [0.3, 0.5, 0.7]

    for discipline in df["discipline"].unique():
        subset = df[df["discipline"] == discipline]

        for rho in selected_rhos:
            data = subset[subset["rho"] == rho].sort_values("M")

            plt.plot(
                data["M"],
                data["mean_simulation_EW"],
                marker="o",
                label=f"{discipline}, ρ={rho}",
            )

    plt.xlabel("Number of stations M")
    plt.ylabel("Average waiting time E[W]")
    plt.title("Waiting time vs number of stations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path = output_dir / "waiting_time_vs_M.png"
    plt.savefig(output_path, dpi=300)
    plt.close()


def main() -> None:
    input_path = PROJECT_ROOT / "outputs" / "tables" / "summary_results.csv"
    output_dir = PROJECT_ROOT / "outputs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    plot_waiting_time_vs_rho(df, output_dir)
    plot_relative_error_vs_rho(df, output_dir)
    plot_waiting_time_vs_M(df, output_dir)

    print("Figures saved in:")
    print(output_dir)


if __name__ == "__main__":
    main()