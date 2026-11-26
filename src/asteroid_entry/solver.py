"""High-level orchestration of atmospheric entry simulations.

This module defines the public interface for performing an atmospheric
entry simulation using specified initial conditions, physical models
and numerical integration settings.
"""

from asteroid_entry.conditions import EntryConditions
from asteroid_entry.model import EntryModel
from asteroid_entry.options import SolverOptions
from asteroid_entry.result import SimulationResult


def simulate_entry(
    conditions: EntryConditions,
    *,
    model: EntryModel | None = None,
    options: SolverOptions | None = None,
) -> SimulationResult:
    """Simulate the atmospheric entry of an asteroid.

    Parameters
    ----------
    conditions : EntryConditions
        Initial physical properties and atmospheric entry conditions.
    model : EntryModel or None, optional
        Physical model configuration for the simulation. The default
        is None, indicating that no explicit physical model has been
        supplied.
    options : SolverOptions or None, optional
        Numerical integration and output settings. The default is
        None, indicating that no explicit numerical configuration
        has been supplied.

    Returns
    -------
    SimulationResult
        Intended result of the atmospheric entry simulation. No
        result is currently returned because the solver is
        unimplemented.

    Raises
    ------
    NotImplementedError
        Always, because the simulation solver is not yet implemented.

    See Also
    --------
    asteroid_entry.conditions.EntryConditions
        Initial physical properties and entry conditions.
    asteroid_entry.model.EntryModel
        Physical models and coefficients for atmospheric entry.
    asteroid_entry.options.SolverOptions
        Numerical integration and output settings.
    asteroid_entry.dynamics.rhs
        Evaluation of the continuous state derivatives.

    Notes
    -----
    This function is intended to coordinate state initialisation,
    evaluation of the governing equations, numerical time integration
    and construction of the simulation result.

    The handling of default configurations, integration termination
    and simulation output is not yet implemented.
    """
    raise NotImplementedError
