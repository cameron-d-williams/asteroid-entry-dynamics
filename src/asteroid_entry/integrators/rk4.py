"""Classical fourth-order Runge-Kutta integration."""

from collections.abc import Callable

from asteroid_entry.state import FloatArray

RHSFunction = Callable[[float, FloatArray], FloatArray]


def rk4_step(
    rhs: RHSFunction,
    t: float,
    state: FloatArray,
    step_size: float,
) -> FloatArray:
    """Advance an ordinary differential equation by one RK4 step."""
    raise NotImplementedError
