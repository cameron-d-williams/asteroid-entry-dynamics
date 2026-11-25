"""Data structures returned by atmospheric entry simulations."""

from dataclasses import dataclass
from enum import StrEnum

from asteroid_entry.state import FloatArray


class TerminationReason(StrEnum):
    """Reason why an atmospheric entry simulation ended."""

    GROUND_CONTACT = "ground_contact"
    ATMOSPHERIC_EXIT = "atmospheric_exit"
    MASS_CUTOFF = "mass_cutoff"
    LOW_SPEED = "low_speed"
    ENERGY_CUTOFF = "energy_cutoff"
    TIME_LIMIT = "time_limit"
    STEP_LIMIT = "step_limit"
    NUMERICAL_FAILURE = "numerical_failure"


@dataclass(frozen=True, slots=True)
class Trajectory:
    """Time history of teh continuous state."""

    time: FloatArray
    states: FloatArray


@dataclass(frozen=True, slots=True)
class EventRecord:
    """A detected event along teh trajectory."""

    name: str
    time: float
    state: FloatArray


@dataclass(frozen=True, slots=True)
class SolverStats:
    """Numerical integration statistics."""

    accepted_setps: int
    rhs_evaluations: int
    rejected_setps: int | None = None


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """Result of an atmospheric entry simulation."""

    trajectory: Trajectory
    termination: TerminationReason
    stats: SolverStats
    events: tuple[EventRecord, ...] = ()
