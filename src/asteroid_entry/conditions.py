"""Initial conditions for atmospheric entry simulations.

This module defines the initial physical properties and entry conditions
of an asteroid. All dimensional quantities are expressed in SI units.
"""

from dataclasses import dataclass


# Static docstring validation cannot infer the generated constructor.
@dataclass(frozen=True, slots=True, kw_only=True)
class EntryConditions:  # numpydoc ignore=PR02
    """Initial physical properties and entry conditions of an asteroid.

    Parameters are keyword-only and cannot be reassigned after
    initialisation.

    Parameters
    ----------
    radius : float
        Initial asteroid radius (m).
    velocity : float
        Initial asteroid speed (m s^-1).
    density : float
        Initial asteroid bulk mass density (kg m^-3).
    strength : float
        Asteroid material strength (Pa).
    angle_rad : float
        Initial atmospheric entry angle (rad).
    altitude : float, optional
        Initial geometric altitude relative to the planetary reference
        surface (m). The default is 100000.0.

    Attributes
    ----------
    radius : float
        Initial asteroid radius (m).
    velocity : float
        Initial asteroid speed (m s^-1).
    density : float
        Initial asteroid bulk mass density (kg m^-3).
    strength : float
        Asteroid material strength (Pa).
    angle_rad : float
        Initial atmospheric entry angle (rad).
    altitude : float
        Initial geometric altitude relative to the planetary reference
        surface (m).

    Notes
    -----
    This class stores the initial conditions without validating their
    physical admissibility.
    """

    radius: float
    velocity: float
    density: float
    strength: float
    angle_rad: float
    altitude: float = 100_000.0
