"""Atmospheric density models."""

from dataclasses import dataclass
from typing import Protocol


class Atmosphere(Protocol):
    """Interface for atmospheric density models."""

    def density(self, altitude: float) -> float:
        """Return atmospheric density in kg/m^3."""
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
class ConstantAtmosphere:
    """Atmosphere with altitude-independent density."""

    surface_density: float = 1.2

    def density(self, altitude: float) -> float:
        """Return atmospheric density in kg/m^3."""
        raise NotImplementedError


@dataclass(frozen=True, slots=True, kw_only=True)
class ExponentialAtmosphere:
    """Atmosphere with a constant density scale height."""

    surface_density: float = 1.2
    scale_height = 8_000.0

    def density(self, altitude: float) -> float:
        """Return atmospheric density in kg/m^3."""
        raise NotImplementedError
