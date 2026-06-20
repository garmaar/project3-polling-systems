# Polling Systems: Simulation and Validation

Wireless Internet Practical Project 3 — Academic Year 2025/2026

## Overview

This repository contains a discrete-event simulation of polling-based multiple access systems.

The goal of the project is to implement a simple but complete polling system simulator, evaluate its performance, and compare the simulation results with the analytical models studied during the course.

The simulator supports:

* Multiple stations
* Poisson packet arrivals
* Configurable traffic load
* Configurable service time
* Configurable switching time
* Exhaustive polling
* Limited polling / round-robin polling
* Average packet waiting time computation
* Per-station statistics
* Comparison with theoretical results
* Parameter sweep experiments
* Extension scenario with one highly loaded station

## Project Objective

The project analyzes polling systems where a single server visits several stations cyclically.

At each station, packets wait in a queue until the server arrives. The server then serves packets according to the selected polling discipline.

The two implemented service disciplines are:

1. **Exhaustive polling**
   The server serves all packets waiting in the current station before moving to the next one.

2. **Limited polling / round-robin polling**
   The server serves at most `k` packets per visit. In this project, the default value is `k = 1`.

The main performance metric is the average packet waiting time:

```text
W = service_start_time - arrival_time
```

## Repository Structure

```text
PollingProject/
│
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
│
├── src/
│   ├── config.py
│   ├── packet.py
│   ├── station.py
│   ├── simulation.py
│   ├── disciplines.py
│   ├── metrics.py
│   └── theory.py
│
├── experiments/
│   ├── run_experiments.py
│   ├── analyze_results.py
│   ├── plot_results.py
│   ├── run_extension.py
│   └── plot_extension.py
│
├── notebooks/
│   └── project3_analysis.ipynb
│
├── outputs/
│   ├── raw/
│   │   └── experiment_results.csv
│   ├── tables/
│   │   └── summary_results.csv
│   └── figures/
│       ├── ew_vs_rho.png
│       ├── ew_vs_M.png
│       ├── simulation_vs_theory.png
│       ├── relative_error.png
│       └── extension_fairness.png
│
└── report/
    └── final_report.pdf
```

## Architecture

The project is divided into two independent layers.

### Part A — Minimal Working Simulation Program

This part contains the core simulator. It is designed to run independently before any analysis or report-generation code is added.

Implemented components:

| Component             | File                 | Description                                                     |
| --------------------- | -------------------- | --------------------------------------------------------------- |
| Configuration block   | `src/config.py`      | Stores simulation parameters using a dataclass                  |
| Packet object         | `src/packet.py`      | Represents individual packets and their timestamps              |
| Station block         | `src/station.py`     | Represents each station queue                                   |
| Arrival process       | `src/simulation.py`  | Generates Poisson arrivals using exponential interarrival times |
| Polling server        | `src/simulation.py`  | Visits stations cyclically                                      |
| Exhaustive discipline | `src/disciplines.py` | Serves packets until the station queue is empty                 |
| Limited discipline    | `src/disciplines.py` | Serves at most `k` packets per visit                            |
| Statistics block      | `src/metrics.py`     | Computes waiting time and per-station metrics                   |
| Theory block          | `src/theory.py`      | Computes theoretical waiting time predictions                   |
| Main execution        | `main.py`            | Runs one simulation scenario from the command line              |

### Part B — Analysis and Report Layer

This part is used to run multiple experiments, aggregate results, generate figures, study the extension scenario, and prepare the final report.

Implemented or planned components:

| Component                 | File                                | Description                                                 |
| ------------------------- | ----------------------------------- | ----------------------------------------------------------- |
| Experiment manager        | `experiments/run_experiments.py`    | Runs several scenarios automatically                        |
| Result aggregation        | `experiments/analyze_results.py`    | Aggregates results over different random seeds              |
| Main plot generation      | `experiments/plot_results.py`       | Generates the main validation and performance figures       |
| Extension scenario        | `experiments/run_extension.py`      | Evaluates asymmetric traffic with one highly loaded station |
| Extension plot generation | `experiments/plot_extension.py`     | Generates fairness and per-station waiting time figures     |
| Notebook analysis         | `notebooks/project3_analysis.ipynb` | Contains plots, explanations, and final discussion          |

## How to Run the Project

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run one basic simulation scenario

Run exhaustive polling:

```powershell
python main.py 1
```

Run limited polling:

```powershell
python main.py 2
```

### 5. Run the full experiment set

```powershell
python experiments/run_experiments.py
```

### 6. Analyze the experiment results

```powershell
python experiments/analyze_results.py
```

### 7. Generate the main plots

```powershell
python experiments/plot_results.py
```

### 8. Run the extension scenario

```powershell
python experiments/run_extension.py
```

### 9. Generate the extension plots

```powershell
python experiments/plot_extension.py
```

## Requirements

The project uses the following Python packages:

```text
simpy
numpy
pandas
matplotlib
jupyter
```

A possible `requirements.txt` file is:

```text
simpy
numpy
pandas
matplotlib
jupyter
```

## Main Simulation Parameters

The main configurable parameters are:

| Parameter         | Meaning                                                       |
| ----------------- | ------------------------------------------------------------- |
| `M`               | Number of stations                                            |
| `rho`             | Total system load                                             |
| `T`               | Packet service time                                           |
| `h`               | Switching time between stations                               |
| `discipline`      | Polling discipline: exhaustive or limited                     |
| `k`               | Maximum number of packets served per visit in limited polling |
| `simulation_time` | Total simulated time                                          |
| `warmup_time`     | Initial transient period discarded from statistics            |
| `seed`            | Random seed used for reproducibility                          |

## Running Custom Scenarios

Run exhaustive polling with custom parameters:

```powershell
python main.py 1 --M 20 --rho 0.6 --T 3 --h 0.8
```

Run limited polling with custom parameters:

```powershell
python main.py 2 --M 10 --rho 0.7 --T 3 --h 0.8 --k 1
```

Command line discipline codes:

| Code | Discipline         |
| ---- | ------------------ |
| `1`  | Exhaustive polling |
| `2`  | Limited polling    |

## Reference Validation Scenario

The simulator was validated using the following reference scenario:

```text
M = 10
T = 3
h = 0.8
rho = 0.7
k = 1
```

### Exhaustive polling

```text
Simulation E[W] ≈ 15.82
Theory E[W]     ≈ 15.90
Relative error  ≈ 0.48 %
```

### Limited polling

```text
Simulation E[W] ≈ 46.73
Theory E[W]     ≈ 47.03
Relative error  ≈ 0.65 %
```

These results show that the simulator agrees closely with the theoretical model for the selected reference scenario.

## Experiment Set

The experiment manager runs several combinations of parameters.

Parameter sweep:

```text
Disciplines: exhaustive, limited
M values:    5, 10, 20
rho values:  0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7
Seeds:       1, 2, 3
```

The raw output is stored in:

```text
outputs/raw/experiment_results.csv
```

The stored fields include:

* discipline
* M
* rho
* T
* h
* k
* seed
* simulation_EW
* theoretical_EW
* absolute_error
* relative_error
* packet count

## Result Aggregation

After running the experiments, the results are aggregated over different seeds.

The aggregated output is stored in:

```text
outputs/tables/summary_results.csv
```

The summary includes:

* mean simulated waiting time
* standard deviation
* mean theoretical waiting time
* mean absolute error
* mean relative error
* maximum relative error
* mean packet count
* number of runs

## Figures

The main generated figures are stored in:

```text
outputs/figures/
```

Main figures:

* `ew_vs_rho.png`
* `ew_vs_M.png`
* `simulation_vs_theory.png`
* `relative_error.png`
* `extension_fairness.png`

## Extension Scenario

The extension considers an asymmetric traffic scenario where one station generates significantly more traffic than the others.

Example:

```text
lambda_hot = alpha * lambda_normal
```

The goal is to evaluate:

* waiting time per station
* fairness across stations
* behavior under exhaustive polling
* behavior under limited polling

Expected qualitative behavior:

* Exhaustive polling tends to help the highly loaded station because the server remains there until its queue is empty.
* Limited polling provides more regular service opportunities to all stations.
* Under limited polling, the highly loaded station may experience a much higher waiting time.
* Exhaustive polling may be efficient for the hot station but less fair for the rest.

## Fairness Metrics

The extension uses per-station waiting times and fairness indicators.

Possible metrics:

```text
max/min waiting time ratio
Jain fairness index
```

Jain's fairness index is computed as:

```text
J = (sum(x_i)^2) / (M * sum(x_i^2))
```

where `x_i` represents the performance value of station `i`.

## Notebook

The notebook is located in:

```text
notebooks/project3_analysis.ipynb
```

It is used for:

* loading experiment results
* displaying tables
* generating or showing plots
* comparing simulation and theory
* analyzing the impact of traffic load
* analyzing the impact of the number of stations
* discussing exhaustive vs limited polling
* presenting the extension scenario
* preparing the final report material

The notebook should not contain the main simulator logic. The simulator logic is implemented in `src/`.

## Report

The final report should be concise and limited to a maximum of 3 pages.

Suggested structure:

1. **Model and implementation**

   * Polling system description
   * Poisson arrivals
   * Service disciplines
   * Simulation parameters

2. **Validation and performance results**

   * Simulation vs theory
   * Average waiting time
   * Impact of traffic load
   * Impact of number of stations

3. **Extension and conclusions**

   * Asymmetric traffic scenario
   * Per-station waiting time
   * Fairness comparison
   * Final conclusions

## Current Status

Completed:

* Core simulator architecture
* SimPy implementation
* Poisson arrivals
* Multiple stations
* Exhaustive polling
* Limited polling
* Packet logging
* Waiting-time computation
* Theory comparison
* CLI parameterization
* Experiment manager
* Seed aggregation

Pending:

* Plot generation
* Extension scenario
* Fairness analysis
* Final notebook polishing
* Final report generation

## Main Conclusion

The simulator has been validated against the analytical model in a reference scenario. Both exhaustive and limited polling produce relative errors below 1%, which confirms that the simulation implementation is consistent with the theoretical predictions.

The next step is to use the validated simulator to study how polling performance changes with traffic load, number of stations, and asymmetric traffic conditions.
