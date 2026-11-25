"""Gravitational acceleration models"""

from dataclasses import dataclass
from typing import Protocol


class Gravity(Protocol):
    """Interface for gravitational acceleration models."""

    def acceleration(
        self,
        altitude: float,
        *,
        planet_radius: float,
    ) -> float:
        """Return gravitational acceleration in m/s2."""
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
class ConstantGravity:
    """Altitude independent gravitational acceleration model"""

    g0: float = 9.81

    def acceleration(
        self,
        altitude: float,
        *,
        planet_radius: float,
    ) -> float:
        """Return gravitational acceleration in m/s2."""
        raise NotImplementedError
