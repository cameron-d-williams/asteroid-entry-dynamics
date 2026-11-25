"""Numerical simulation of asteroid atmospheric entry."""

from asteroid_entry.atmosphere import (
    ConstantAtmosphere,
    ExponentialAtmosphere,
)
from asteroid_entry.conditions import EntryConditions
from asteroid_entry.gravity import ConstantGravity
from asteroid_entry.model import EntryModel
from asteroid_entry.options import SolverOptions
from asteroid_entry.result import (
    EventRecord,
    SimulationResult,
    SolverStats,
    TerminationReason,
    Trajectory,
)
from asteroid_entry.solver import simulate_entry

__all__ = [
    "ConstantAtmosphere",
    "ConstantGravity",
    "EntryConditions",
    "EntryModel",
    "EventRecord",
    "ExponentialAtmosphere",
    "SimulationResult",
    "SolverOptions",
    "SolverStats",
    "TerminationReason",
    "Trajectory",
    "simulate_entry",
]
