"""Numerical configuration for atmospheric entry simulations.

This module defines the configuration parameters for numerical time
integration and simulation output.
"""

from dataclasses import dataclass
from typing import Literal


# Static docstring validation cannot infer the generated constructor.
@dataclass(frozen=True, slots=True, kw_only=True)
class SolverOptions:  # numpydoc ignore=PR02
    """Numerical integration and output settings.

    Parameters are keyword-only and cannot be reassigned after
    initialisation.

    Parameters
    ----------
    method : {'rk4'}
        Numerical time integration method. The currently declared
        option is the classical fourth-order Runge-Kutta method.
    step_size : float, optional
        Integration time step (s). The default is 0.01.
    output_dt : float or None, optional
        Requested time interval between simulation outputs (s).
        The default is None, indicating that no explicit output
        interval has been specified.
    max_time : float, optional
        Maximum simulation duration (s). The default is 1000.0.

    Attributes
    ----------
    method : {'rk4'}
        Numerical time integration method.
    step_size : float
        Integration time step (s).
    output_dt : float or None
        Requested time interval between simulation outputs (s).
    max_time : float
        Maximum simulation duration (s).

    Notes
    -----
    This class stores numerical configuration parameters without
    performing runtime validation. The interpretation and enforcement
    of these settings are the responsibility of the solver.
    """

    method: Literal["rk4"]
    step_size: float = 0.01
    output_dt: float | None = None
    max_time: float = 1_000.0
