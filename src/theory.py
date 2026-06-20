from src.config import SimulationConfig


def exhaustive_waiting_time(config: SimulationConfig) -> float:
    rho = config.load
    T = config.service_time
    h = config.switch_time
    M = config.num_stations

    if rho >= 1:
        raise ValueError("Unstable exhaustive polling system: rho >= 1.")

    return (rho * T) / (2 * (1 - rho)) + ((M - rho) * h) / (2 * (1 - rho))


def limited_waiting_time(config: SimulationConfig) -> float:
    rho = config.load
    T = config.service_time
    h = config.switch_time
    M = config.num_stations

    rho_max = T / (T + h)

    if rho >= rho_max:
        raise ValueError(
            f"Unstable limited polling system: rho >= rho_max = {rho_max:.4f}"
        )

    denominator = 2 * (1 - rho * (T + h) / T)

    return (rho * (T + h) + M * h) / denominator


def theoretical_waiting_time(config: SimulationConfig) -> float:
    if config.discipline == "exhaustive":
        return exhaustive_waiting_time(config)

    if config.discipline == "limited":
        return limited_waiting_time(config)

    raise ValueError(f"Unknown discipline: {config.discipline}")