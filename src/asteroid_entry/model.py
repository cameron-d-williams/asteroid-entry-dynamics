"""Physical configuration for atmospheric entry simulations."""

from dataclasses import dataclass, field

from asteroid_entry.atmosphere import Atmosphere, ExponentialAtmosphere
from asteroid_entry.gravity import ConstantGravity, Gravity


@dataclass(frozen=True, slots=True, kw_only=True)
class EntryModel:
    """Physical models and coefficients for atmospheric entry."""

    atmosphere: Atmosphere = field(default_factory=ExponentialAtmosphere)
    gravity: Gravity = field(default_factory=ConstantGravity)

    planet_radius: float = 6_371_000.0

    drag_coefficient: float = 1.0
    heat_transfer_coefficient: float = 1.0
    lift_coefficient: float = 1.0
    heat_of_ablation: float = 1e7

    pancake_factor: float = 6.5
    fragmentation_enabled: bool = False
