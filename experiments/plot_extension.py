from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def plot_per_station_waiting_time(df: pd.DataFrame, output_dir: Path) -> None:
    averaged = (
        df.groupby(["discipline", "station_id", "is_hot_station"])
        .agg(mean_waiting_time=("waiting_time", "mean"))
        .reset_index()
    )

    plt.figure()

    for discipline in ["exhaustive", "limited"]:
        data = averaged[averaged["discipline"] == discipline].sort_values("station_id")

        plt.plot(
            data["station_id"],
            data["mean_waiting_time"],
            marker="o",
            label=discipline,
        )

    plt.xlabel("Station ID")
    plt.ylabel("Average waiting time E[W_i]")
    plt.title("Extension: per-station waiting time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path = output_dir / "extension_per_station_waiting_time.png"
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_fairness(df: pd.DataFrame, output_dir: Path) -> None:
    averaged = (
        df.groupby("discipline")
        .agg(
            hot_station_waiting_time=("hot_station_waiting_time", "mean"),
            normal_mean_waiting_time=("normal_mean_waiting_time", "mean"),
            max_min_ratio=("max_min_ratio", "mean"),
            jain_fairness_index=("jain_fairness_index", "mean"),
        )
        .reset_index()
    )

    plt.figure()

    x = range(len(averaged))

    plt.bar(
        [i - 0.2 for i in x],
        averaged["hot_station_waiting_time"],
        width=0.4,
        label="Hot station",
    )

    plt.bar(
        [i + 0.2 for i in x],
        averaged["normal_mean_waiting_time"],
        width=0.4,
        label="Normal stations mean",
    )

    plt.xticks(list(x), averaged["discipline"])
    plt.ylabel("Average waiting time")
    plt.title("Extension: hot station vs normal stations")
    plt.legend()
    plt.grid(axis="y")
    plt.tight_layout()

    output_path = output_dir / "extension_hot_vs_normal.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    fairness_path = output_dir / "extension_fairness_summary.csv"
    averaged.to_csv(fairness_path, index=False)


def main() -> None:
    input_dir = PROJECT_ROOT / "outputs" / "tables"
    output_dir = PROJECT_ROOT / "outputs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    per_station_path = input_dir / "extension_per_station.csv"
    fairness_path = input_dir / "extension_fairness.csv"

    per_station_df = pd.read_csv(per_station_path)
    fairness_df = pd.read_csv(fairness_path)

    plot_per_station_waiting_time(per_station_df, output_dir)
    plot_fairness(fairness_df, output_dir)

    print("Extension figures saved in:")
    print(output_dir)


if __name__ == "__main__":
    main()