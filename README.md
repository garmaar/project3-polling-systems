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
│   ├── __init__.py
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
│   └── run_hot_station.py
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
│       └── hot_station_fairness.png
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

| Component            | File                                | Description                                        |
| -------------------- | ----------------------------------- | -------------------------------------------------- |
| Experiment manager   | `experiments/run_experiments.py`    | Runs several scenarios automatically               |
| Result aggregation   | `experiments/analyze_results.py`    | Aggregates results over different random seeds     |
| Plot generation      | `experiments/plot_results.py`       | Generates final figures                            |
| Hot-station scenario | `experiments/run_hot_station.py`    | Evaluates asymmetric traffic load                  |
| Notebook analysis    | `notebooks/project3_analysis.ipynb` | Contains plots, explanations, and final discussion |

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

On Windows:

```bash
.venv\Scripts\activate
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running One Simulation Scenario

Run exhaustive polling:

```bash
python main.py 1
```

Run limited polling:

```bash
python main.py 2
```

Run exhaustive polling with custom parameters:

```bash
python main.py 1 --M 20 --rho 0.6 --T 3 --h 0.8
```

Run limited polling with custom parameters:

```bash
python main.py 2 --M 10 --rho 0.7 --T 3 --h 0.8 --k 1
```

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
* Hot-station extension
* Fairness analysis
* Final notebook polishing
* Final report generation
