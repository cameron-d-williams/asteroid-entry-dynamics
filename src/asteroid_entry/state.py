"""State representation and initialisation for atmospheric entry.

This module defines the continuous state vector indices, discrete
physical modes and initial state construction interface.

Continuous state arrays use the `FloatArray` type alias, representing
NumPy arrays with a float64 data type.
"""

from enum import IntEnum, StrEnum

import numpy as np
from numpy.typing import NDArray

from asteroid_entry.conditions import EntryConditions

FloatArray = NDArray[np.float64]


# Inherited enumeration constructor arguments are not part of the API
# being documented.
class StateIndex(IntEnum):  # numpydoc ignore=PR01
    """Indices of the continuous state variables.

    Attributes
    ----------
    VELOCITY : int
        Index of the asteroid speed (m s^-1).
    MASS : int
        Index of the asteroid mass (kg).
    ANGLE : int
        Index of the atmospheric entry angle (rad).
    ALTITUDE : int
        Index of the geometric altitude (m).
    DISTANCE : int
        Index of the distance variable (m).
    RADIUS : int
        Index of the asteroid radius (m).
    SPREADING_RATE : int
        Index of the radial spreading rate (m s^-1).

    Notes
    -----
    The enumeration defines the ordering of the seven continuous
    state variables. Its integer values can be used directly to
    index the state vector.
    """

    VELOCITY = 0
    MASS = 1
    ANGLE = 2
    ALTITUDE = 3
    DISTANCE = 4
    RADIUS = 5
    SPREADING_RATE = 6


# Inherited enumeration constructor arguments are not part of the API
# being documented.
class EntryMode(StrEnum):  # numpydoc ignore=PR01
    """Discrete physical modes of the entry system.

    Attributes
    ----------
    INTACT : str
        Intact asteroid mode.
    SPREADING : str
        Radial spreading mode.
    SATURATED : str
        Saturated spreading mode.

    Notes
    -----
    The enumeration identifies the discrete physical modes separately
    from the continuous state vector. The criteria governing
    transitions between these modes are not defined in this module.
    """

    INTACT = "intact"
    SPREADING = "spreading"
    SATURATED = "saturated"


def initial_state(conditions: EntryConditions) -> FloatArray:
    """Construct the initial continuous state vector.

    Parameters
    ----------
    conditions : EntryConditions
        Initial physical properties and atmospheric entry conditions.

    Returns
    -------
    FloatArray
        Intended initial state vector of shape (7,) and float64 data
        type, ordered according to :class:`StateIndex`. No array is
        currently returned because the function is unimplemented.

    Raises
    ------
    NotImplementedError
        Always, because initial state construction is not yet
        implemented.

    See Also
    --------
    StateIndex : Indices of the continuous state variables.
    asteroid_entry.conditions.EntryConditions
        Initial physical properties and entry conditions.
    """
    raise NotImplementedError
