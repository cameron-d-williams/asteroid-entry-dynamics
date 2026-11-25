"""Initial conditions for atmospheric entry simulations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class EntryConditions:
    """Initial physical properties and entry conditions."""

    radius: float
    velocity: float
    density: float
    strength: float
    angle_rad: float
    altitude: float = 100_000.0
