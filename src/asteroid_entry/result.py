"""Data structures returned by atmospheric entry simulations.

This module defines the trajectory, event records, numerical
integration statistics and termination reasons associated with an
atmospheric entry simulation.
"""

from dataclasses import dataclass
from enum import StrEnum

from asteroid_entry.state import FloatArray


# Inherited enumeration constructor arguments are not part of the API
# being documented.
class TerminationReason(StrEnum):  # numpydoc ignore=PR01
    """Reason why an atmospheric entry simulation ended.

    Attributes
    ----------
    GROUND_CONTACT : str
        Contact with the planetary surface.
    ATMOSPHERIC_EXIT : str
        Exit from the modelled atmosphere.
    MASS_CUTOFF : str
        Attainment of the mass termination threshold.
    LOW_SPEED : str
        Attainment of the speed termination threshold.
    ENERGY_CUTOFF : str
        Attainment of the energy termination threshold.
    TIME_LIMIT : str
        Attainment of the simulation time limit.
    STEP_LIMIT : str
        Attainment of the numerical integration step limit.
    NUMERICAL_FAILURE : str
        Failure of the numerical integration procedure.

    Notes
    -----
    This enumeration defines the possible termination reasons.
    The corresponding termination criteria and thresholds are
    not defined in this module.
    """

    GROUND_CONTACT = "ground_contact"
    ATMOSPHERIC_EXIT = "atmospheric_exit"
    MASS_CUTOFF = "mass_cutoff"
    LOW_SPEED = "low_speed"
    ENERGY_CUTOFF = "energy_cutoff"
    TIME_LIMIT = "time_limit"
    STEP_LIMIT = "step_limit"
    NUMERICAL_FAILURE = "numerical_failure"


# Static docstring validation cannot infer the generated constructor.
@dataclass(frozen=True, slots=True)
class Trajectory:  # numpydoc ignore=PR02
    """Time history of the continuous state.

    Parameters
    ----------
    time : FloatArray
        Simulation times associated with the recorded states (s).
    states : FloatArray
        Recorded continuous state vectors, with state variables
        ordered according to :class:`asteroid_entry.state.StateIndex`.

    Attributes
    ----------
    time : FloatArray
        Recorded simulation times (s).
    states : FloatArray
        Recorded continuous state vectors.

    Notes
    -----
    This class stores trajectory arrays without validating their
    shapes, ordering or mutual consistency.

    The attributes cannot be reassigned after initialisation.
    However, this does not make the underlying NumPy arrays immutable.
    """

    time: FloatArray
    states: FloatArray


# Static docstring validation cannot infer the generated constructor.
@dataclass(frozen=True, slots=True)
class EventRecord:  # numpydoc ignore=PR02
    """Record of a detected event along the trajectory.

    Parameters
    ----------
    name : str
        Identifier of the detected event.
    time : float
        Simulation time at which the event occurred (s).
    state : FloatArray
        Continuous state vector at the event time, ordered according
        to :class:`asteroid_entry.state.StateIndex`.

    Attributes
    ----------
    name : str
        Event identifier.
    time : float
        Event time (s).
    state : FloatArray
        Continuous state vector at the event time.

    Notes
    -----
    This class stores event information without performing event
    detection or validating the supplied state.
    """

    name: str
    time: float
    state: FloatArray


# Static docstring validation cannot infer the generated constructor.
@dataclass(frozen=True, slots=True)
class SolverStats:  # numpydoc ignore=PR02
    """Numerical integration statistics.

    Parameters
    ----------
    accepted_setps : int
        Number of accepted numerical integration steps.
    rhs_evaluations : int
        Number of right-hand side function evaluations.
    rejected_setps : int or None, optional
        Number of rejected numerical integration steps. The default
        is None, indicating that no rejection count has been supplied.

    Attributes
    ----------
    accepted_setps : int
        Number of accepted integration steps.
    rhs_evaluations : int
        Number of right-hand side function evaluations.
    rejected_setps : int or None
        Number of rejected integration steps, if supplied.

    Notes
    -----
    This class stores integration statistics without validating
    their values or calculating them independently.
    """

    accepted_setps: int
    rhs_evaluations: int
    rejected_setps: int | None = None


# Static docstring validation cannot infer the generated constructor.
@dataclass(frozen=True, slots=True)
class SimulationResult:  # numpydoc ignore=PR02
    """Result of an atmospheric entry simulation.

    Parameters
    ----------
    trajectory : Trajectory
        Recorded time history of the continuous state.
    termination : TerminationReason
        Reason for simulation termination.
    stats : SolverStats
        Numerical integration statistics.
    events : tuple of EventRecord, optional
        Recorded simulation events. The default is an empty tuple.

    Attributes
    ----------
    trajectory : Trajectory
        Recorded simulation trajectory.
    termination : TerminationReason
        Simulation termination reason.
    stats : SolverStats
        Numerical integration statistics.
    events : tuple of EventRecord
        Recorded simulation events.

    See Also
    --------
    Trajectory : Time history of the continuous state.
    TerminationReason : Reason for simulation termination.
    SolverStats : Numerical integration statistics.
    EventRecord : Record of a detected event along the trajectory.

    Notes
    -----
    This class aggregates the outputs associated with a simulation
    without performing additional calculations or validation.
    """

    trajectory: Trajectory
    termination: TerminationReason
    stats: SolverStats
    events: tuple[EventRecord, ...] = ()
