"""Classical fourth-order Runge-Kutta integration.

This module defines the interface for advancing a system of
first-order ordinary differential equations using the classical
fourth-order Runge-Kutta method.

The `RHSFunction` type alias represents a callable that accepts
the current time and state vector and returns the corresponding
time derivatives.
"""

from collections.abc import Callable

from asteroid_entry.state import FloatArray

RHSFunction = Callable[[float, FloatArray], FloatArray]


def rk4_step(
    rhs: RHSFunction,
    t: float,
    state: FloatArray,
    step_size: float,
) -> FloatArray:
    r"""Advance an ordinary differential equation by one RK4 step.

    Parameters
    ----------
    rhs : RHSFunction
        Right-hand side function accepting the current time and
        state vector and returning a derivative vector of the
        same shape as the state vector.
    t : float
        Current integration time (s).
    state : FloatArray
        Current continuous state vector of shape (n,) and float64
        data type, where n is the number of state variables.
    step_size : float
        Integration time step (s).

    Returns
    -------
    FloatArray
        Intended state vector at time ``t + step_size``, with the
        same shape and data type as `state`. No array is currently
        returned because the function is unimplemented.

    Raises
    ------
    NotImplementedError
        Always, because the numerical integration method is not
        yet implemented.

    Notes
    -----
    The classical fourth-order Runge-Kutta method is intended to
    advance the solution of a system of first-order ordinary
    differential equations of the form

    .. math::

        \frac{\mathrm{d}\mathbf{y}}{\mathrm{d}t}
        = \mathbf{f}(t, \mathbf{y}),

    where :math:`t` is the integration time, :math:`\mathbf{y}` is
    the continuous state vector and :math:`\mathbf{f}` is the
    right-hand side function.

    The numerical integration algorithm is not yet implemented.
    """
    raise NotImplementedError
