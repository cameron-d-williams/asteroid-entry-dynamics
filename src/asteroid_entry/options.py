"""Numerica configuration for atmospheric entry simulations."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True, kw_only=True)
class SolverOptions:
    """Numerical integration and output settings"""

    method: Literal["rk4"]
    step_size: float = 0.01
    output_dt: float | None = None
    max_time: float = 1_000.0
