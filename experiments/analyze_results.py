import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


def main() -> None:
    input_path = PROJECT_ROOT / "outputs" / "tables" / "experiment_results.csv"
    output_path = PROJECT_ROOT / "outputs" / "tables" / "summary_results.csv"

    df = pd.read_csv(input_path)

    summary = (
        df.groupby(["discipline", "M", "rho", "T", "h", "k"])
        .agg(
            mean_simulation_EW=("simulation_EW", "mean"),
            std_simulation_EW=("simulation_EW", "std"),
            mean_theoretical_EW=("theoretical_EW", "mean"),
            mean_absolute_error=("absolute_error", "mean"),
            mean_relative_error=("relative_error", "mean"),
            max_relative_error=("relative_error", "max"),
            mean_num_packets=("num_packets", "mean"),
            num_runs=("seed", "count"),
        )
        .reset_index()
    )

    summary.to_csv(output_path, index=False)

    print("=== SUMMARY GENERATED ===")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print()
    print(summary.head(20).to_string(index=False))


if __name__ == "__main__":
    main()