"""Gravitational acceleration models for atmospheric entry simulations.

This module defines the structural interface for gravitational
acceleration models and provides a preliminary constant-gravity model.

All dimensional quantities are expressed in SI units.
"""

from dataclasses import dataclass
from typing import Protocol


# Protocol constructor arguments are not part of the public interface.
class Gravity(Protocol):  # numpydoc ignore=PR01
    """Structural interface for gravitational acceleration models.

    Implementations provide an :meth:`acceleration` method for
    evaluating gravitational acceleration at a specified geometric
    altitude.
    """

    def acceleration(
        self,
        altitude: float,
        *,
        planet_radius: float,
    ) -> float:
        """Evaluate gravitational acceleration.

        Parameters
        ----------
        altitude : float
            Geometric altitude relative to the planetary reference
            surface (m).
        planet_radius : float
            Planetary radius at the reference surface (m).

        Returns
        -------
        float
            Gravitational acceleration (m s^-2).
        """
        ...


# Static docstring validation cannot infer the generated constructor.
@dataclass(frozen=True, slots=True, kw_only=True)
class ConstantGravity:  # numpydoc ignore=PR02
    """Altitude-independent gravitational acceleration model.

    The acceleration method is not yet implemented.

    Parameters
    ----------
    g0 : float, optional
        Prescribed gravitational acceleration (m s^-2).
        The default is 9.81.

    Attributes
    ----------
    g0 : float
        Prescribed gravitational acceleration (m s^-2).

    See Also
    --------
    Gravity : Structural interface for gravitational acceleration
        models.
    """

    g0: float = 9.81

    def acceleration(
        self,
        altitude: float,
        *,
        planet_radius: float,
    ) -> float:
        """Evaluate constant gravitational acceleration.

        Parameters
        ----------
        altitude : float
            Geometric altitude relative to the planetary reference
            surface (m).
        planet_radius : float
            Planetary radius at the reference surface (m).

        Returns
        -------
        float
            Intended gravitational acceleration (m s^-2). No value
            is currently returned because the method is unimplemented.

        Raises
        ------
        NotImplementedError
            Always, because the method is not yet implemented.
        """
        raise NotImplementedError
