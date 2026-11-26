"""Physical configuration for atmospheric entry simulations.

This module defines the atmospheric and gravitational models,
planetary properties, physical coefficients and fragmentation
settings for an atmospheric entry simulation.

All dimensional quantities are expressed in SI units.
"""

from dataclasses import dataclass, field

from asteroid_entry.atmosphere import Atmosphere, ExponentialAtmosphere
from asteroid_entry.gravity import ConstantGravity, Gravity


# Static docstring validation cannot infer the generated constructor.
@dataclass(frozen=True, slots=True, kw_only=True)
class EntryModel:  # numpydoc ignore=PR02
    """Physical models and coefficients for atmospheric entry.

    Parameters are keyword-only and cannot be reassigned after
    initialisation.

    Parameters
    ----------
    atmosphere : Atmosphere, optional
        Atmospheric density model. The default is a new instance of
        :class:`asteroid_entry.atmosphere.ExponentialAtmosphere`.
    gravity : Gravity, optional
        Gravitational acceleration model. The default is a new
        instance of :class:`asteroid_entry.gravity.ConstantGravity`.
    planet_radius : float, optional
        Planetary reference radius (m). The default is 6371000.0.
    drag_coefficient : float, optional
        Dimensionless aerodynamic drag coefficient. The default
        is 1.0.
    heat_transfer_coefficient : float, optional
        Dimensionless heat transfer coefficient. The default is 1.0.
    lift_coefficient : float, optional
        Dimensionless aerodynamic lift coefficient. The default
        is 1.0.
    heat_of_ablation : float, optional
        Specific energy required for ablation (J kg^-1). The default
        is 1e7.
    pancake_factor : float, optional
        Dimensionless parameter governing the extent of radial
        spreading. The default is 6.5.
    fragmentation_enabled : bool, optional
        Flag indicating whether fragmentation is enabled. The
        default is False.

    Attributes
    ----------
    atmosphere : Atmosphere
        Atmospheric density model.
    gravity : Gravity
        Gravitational acceleration model.
    planet_radius : float
        Planetary reference radius (m).
    drag_coefficient : float
        Dimensionless aerodynamic drag coefficient.
    heat_transfer_coefficient : float
        Dimensionless heat transfer coefficient.
    lift_coefficient : float
        Dimensionless aerodynamic lift coefficient.
    heat_of_ablation : float
        Specific energy required for ablation (J kg^-1).
    pancake_factor : float
        Dimensionless parameter governing the extent of radial
        spreading.
    fragmentation_enabled : bool
        Flag indicating whether fragmentation is enabled.

    See Also
    --------
    asteroid_entry.atmosphere.Atmosphere
        Structural interface for atmospheric density models.
    asteroid_entry.gravity.Gravity
        Structural interface for gravitational acceleration models.

    Notes
    -----
    This class stores physical configuration parameters without
    validating their physical admissibility.

    The interpretation and application of the physical coefficients
    depend on the governing equations. The default gravitational
    model is not yet implemented.
    """

    atmosphere: Atmosphere = field(default_factory=ExponentialAtmosphere)
    gravity: Gravity = field(default_factory=ConstantGravity)

    planet_radius: float = 6_371_000.0

    drag_coefficient: float = 1.0
    heat_transfer_coefficient: float = 1.0
    lift_coefficient: float = 1.0
    heat_of_ablation: float = 1e7

    pancake_factor: float = 6.5
    fragmentation_enabled: bool = False
