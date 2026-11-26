"""Governing equations for atmospheric entry dynamics.

This module defines the interface for evaluating the time derivatives
of the continuous state variables, given the current state, physical
model, initial conditions and discrete entry mode.
"""

from asteroid_entry.conditions import EntryConditions
from asteroid_entry.model import EntryModel
from asteroid_entry.state import EntryMode, FloatArray


def rhs(
    t: float,
    state: FloatArray,
    conditions: EntryConditions,
    model: EntryModel,
    mode: EntryMode,
) -> FloatArray:
    r"""Evaluate the time derivatives of the continuous state.

    Parameters
    ----------
    t : float
        Simulation time (s).
    state : FloatArray
        Current continuous state vector of shape (7,), ordered
        according to :class:`asteroid_entry.state.StateIndex`.
    conditions : EntryConditions
        Initial physical properties and atmospheric entry conditions.
    model : EntryModel
        Physical model configuration for the atmospheric entry
        simulation.
    mode : EntryMode
        Current discrete physical mode of the entry system.

    Returns
    -------
    FloatArray
        Intended vector of continuous state derivatives of shape
        (7,) and float64 data type, with the same ordering as `state`.
        Each component has units of its corresponding state variable
        per second. No array is currently returned because the
        function is unimplemented.

    Raises
    ------
    NotImplementedError
        Always, because the governing equations are not yet
        implemented.

    See Also
    --------
    asteroid_entry.state.StateIndex
        Indices of the continuous state variables.
    asteroid_entry.state.EntryMode
        Discrete physical modes of the entry system.

    Notes
    -----
    This function is intended to evaluate the right-hand side of a
    system of first-order ordinary differential equations of the form

    .. math::

        \frac{\mathrm{d}\mathbf{y}}{\mathrm{d}t}
        = \mathbf{f}(t, \mathbf{y}; \boldsymbol{\lambda}, q),

    where :math:`t` is the simulation time, :math:`\mathbf{y}` is the
    continuous state vector, :math:`\boldsymbol{\lambda}` represents
    the physical model and initial condition parameters, :math:`q`
    is the discrete entry mode and :math:`\mathbf{f}` is the
    right-hand side function.

    The physical governing equations and their dependence on the
    discrete entry mode are not yet implemented.
    """
    raise NotImplementedError
