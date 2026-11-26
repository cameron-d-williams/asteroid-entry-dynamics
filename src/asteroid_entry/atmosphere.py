"""Atmospheric density models for atmospheric entry simulations.

This module provides analytical and empirical models of atmospheric mass
density as a function of geometric altitude.

All models conform to the :class:`Atmosphere` protocol and use SI units.
The treatment of negative altitudes is specific to each model.
"""

from dataclasses import dataclass
from math import exp, pow
from typing import Protocol


# Protocol constructor arguments are not part of the public interface.
class Atmosphere(Protocol):  # numpydoc ignore=PR01
    """Structural interface for atmospheric density models.

    Implementations provide a :meth:`density` method for evaluating
    atmospheric mass density at a specified geometric altitude. Each
    model defines its own treatment of negative altitudes.
    """

    def density(self, altitude: float) -> float:
        """Evaluate atmospheric mass density.

        Parameters
        ----------
        altitude : float
            Finite geometric altitude relative to the planetary
            reference surface (m).

        Returns
        -------
        float
            Atmospheric mass density (kg m^-3).
        """
        ...


# Static docstring validation cannot infer the generated constructor.
@dataclass(frozen=True, slots=True, kw_only=True)
class ConstantAtmosphere:  # numpydoc ignore=PR02
    r"""Atmosphere with altitude-independent mass density.

    Parameters are keyword-only and cannot be reassigned after
    initialization.

    Parameters
    ----------
    surface_density : float, optional
        Constant atmospheric mass density (kg m^-3). Must be finite
        and non-negative for physical validity. The default is 1.2.

    Attributes
    ----------
    surface_density : float
        Constant atmospheric mass density (kg m^-3).

    See Also
    --------
    Atmosphere : Structural interface for atmospheric density models.
    ExponentialAtmosphere : Atmosphere with a constant scale height.

    Notes
    -----
    Atmospheric mass density is given by

    .. math::

        \rho_a(z) = \rho_0,

    where :math:`\rho_a` is the atmospheric mass density, :math:`z` is
    the geometric altitude and :math:`\rho_0` is the prescribed density.

    This model is intended for analytical verification and simplified
    numerical experiments rather than realistic atmospheric modelling.
    Setting `surface_density` to zero represents a vacuum.

    The physical constraint on `surface_density` is not enforced during
    initialisation.

    Examples
    --------
    >>> atmosphere = ConstantAtmosphere(surface_density=0.5)
    >>> atmosphere.density(10_000.0)
    0.5

    >>> vacuum = ConstantAtmosphere(surface_density=0.0)
    >>> vacuum.density(100_000.0)
    0.0
    """

    surface_density: float = 1.2

    def density(self, altitude: float) -> float:
        """Evaluate constant atmospheric mass density.

        Parameters
        ----------
        altitude : float
            Geometric altitude relative to the planetary reference
            surface (m). Retained for interface compatibility; it does
            not affect the returned density.

        Returns
        -------
        float
            Atmospheric mass density (kg m^-3).
        """
        return self.surface_density


# Static docstring validation cannot infer the generated constructor.
@dataclass(frozen=True, slots=True, kw_only=True)
class ExponentialAtmosphere:  # numpydoc ignore=PR02
    r"""Atmosphere with a constant density scale height.

    Parameters are keyword-only and cannot be reassigned after
    initialisation.

    Parameters
    ----------
    surface_density : float, optional
        Atmospheric mass density at zero altitude (kg m^-3). Must be
        finite and non-negative for physical validity. The default is
        1.2.
    scale_height : float, optional
        Atmospheric density scale height (m). Must be finite and
        strictly positive for physical validity. The default is 8000.0.

    Attributes
    ----------
    surface_density : float
        Atmospheric mass density at zero altitude (kg m^-3).
    scale_height : float
        Atmospheric density scale height (m).

    See Also
    --------
    Atmosphere : Structural interface for atmospheric density models.
    ConstantAtmosphere : Altitude-independent atmospheric density model.
    GlennAtmosphere : Three-layer empirical Earth atmosphere model.

    Notes
    -----
    Atmospheric mass density is given by

    .. math::

        \rho_a(z) = \rho_0 \exp\left(-\frac{z}{H}\right),

    where :math:`\rho_a` is the atmospheric mass density, :math:`z` is
    the geometric altitude, :math:`\rho_0` is the density at zero
    altitude and :math:`H` is the density scale height.

    This formulation follows from hydrostatic equilibrium for an
    isothermal ideal gas of constant composition under constant
    gravitational acceleration.

    The model provides a smooth, inexpensive approximation for
    non-negative altitudes without resolving variations in temperature
    or composition. Extrapolation below zero altitude is mathematical
    rather than a physical model of the subsurface.

    The physical constraints on the model parameters are not enforced
    during initialisation.

    Examples
    --------
    >>> atmosphere = ExponentialAtmosphere()
    >>> atmosphere.density(0.0)
    1.2

    >>> round(atmosphere.density(8_000.0), 6)
    0.441455

    >>> round(atmosphere.density(-8_000.0), 6)
    3.261938
    """

    surface_density: float = 1.2
    scale_height: float = 8_000.0

    def density(self, altitude: float) -> float:
        """Evaluate exponential atmospheric mass density.

        Parameters
        ----------
        altitude : float
            Finite geometric altitude relative to the planetary
            reference surface (m). Negative altitudes are extrapolated
            using the same exponential expression.

        Returns
        -------
        float
            Atmospheric mass density (kg m^-3).

        Raises
        ------
        OverflowError
            If the exponential cannot be represented as a float.
        ZeroDivisionError
            If `scale_height` is zero.
        """
        return self.surface_density * exp(-altitude / self.scale_height)


@dataclass(frozen=True, slots=True, kw_only=True)
class GlennAtmosphere:
    r"""Three-layer empirical Earth atmosphere model from NASA Glenn.

    See Also
    --------
    Atmosphere : Structural interface for atmospheric density models.
    ExponentialAtmosphere : Atmosphere with a constant scale height.

    Notes
    -----
    The model uses empirical temperature and pressure expressions from
    NASA Glenn Research Center [1]_. The implementation partitions
    non-negative altitudes into three regions:

    - Troposphere: 0 km to below 11 km.
    - Lower stratosphere: 11 km to below 25 km.
    - Upper stratosphere approximation: 25 km and above.

    Atmospheric mass density is calculated from the ideal gas equation
    of state:

    .. math::

        \rho_a = \frac{p}{R_{\mathrm{air}} T},

    where :math:`\rho_a` is the atmospheric mass density, :math:`p` is
    the pressure in pascals, :math:`T` is the absolute temperature in
    kelvins and :math:`R_{\mathrm{air}}` is the specific gas constant
    for air (286.9 J kg^-1 K^-1).

    The implementation retains the source's approximate temperature
    offset of 273.1 and expresses pressure in pascals rather than
    kilopascals. The independently fitted expressions introduce
    discontinuities at the layer boundaries.

    The uppermost expression is extrapolated without an altitude limit.
    It should not be assumed to represent the mesosphere or thermosphere
    accurately. This extrapolation permits comparison with other models
    but does not establish physical validity at high altitudes.

    References
    ----------
    .. [1] NASA Glenn Research Center, "Earth Atmosphere Equation -
           Metric", Beginner's Guide to Aeronautics.
           https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/earth-atmosphere-equation-metric/

    Examples
    --------
    >>> atmosphere = GlennAtmosphere()
    >>> round(atmosphere.density(0.0), 3)
    1.227

    >>> atmosphere.density(-100.0) == atmosphere.density(0.0)
    True
    """

    def density(self, altitude: float) -> float:
        """Evaluate atmospheric mass density using the Glenn model.

        Parameters
        ----------
        altitude : float
            Finite geometric altitude relative to the Earth's reference
            surface (m). Negative altitudes are evaluated at zero
            altitude.

        Returns
        -------
        float
            Atmospheric mass density (kg m^-3).
        """
        # Use the surface fit for below-surface evaluations.
        altitude = max(altitude, 0.0)

        # Evaluate the appropriate layer fit with temperature in K
        # and pressure in Pa.
        if altitude < 11_000.0:
            # Troposphere.
            temperature = 288.14 - (0.00649 * altitude)
            pressure = 101_290.0 * pow(temperature / 288.08, 5.256)
        elif altitude < 25_000.0:
            # Lower stratosphere.
            temperature = 216.64
            pressure = 22_650.0 * exp(1.73 - (0.000157 * altitude))
        else:
            # Upper stratosphere fit and high-altitude extrapolation.
            temperature = 141.89 + (0.00299 * altitude)
            pressure = 2_488.0 * pow(temperature / 216.6, -11.388)

        return pressure / (286.9 * temperature)
