"""Governing equations for atmospheric entry dynamics."""

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
    """Evaluate the time derivatives of the continuous state."""
    raise NotImplementedError
