"""State representation and initialisation."""

from enum import IntEnum, StrEnum

import numpy as np
from numpy.typing import NDArray

from asteroid_entry.conditions import EntryConditions

FloatArray = NDArray[np.float64]


class StateIndex(IntEnum):
    """Indices of the continuous state variables."""

    VELOCITY = 0
    MASS = 1
    ANGLE = 2
    ALTITUDE = 3
    DISTANCE = 4
    RADIUS = 5
    SPREADING_RATE = 6


class EntryMode(StrEnum):
    """Discrete physical modes of the entry system."""

    INTACT = "intact"
    SPREADING = "spreading"
    SATURATED = "saturated"


def initial_state(conditions: EntryConditions) -> FloatArray:
    """Construct the initial continuous state vector."""
    raise NotImplementedError
