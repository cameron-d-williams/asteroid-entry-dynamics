"""High-level orchestration of atmospheric entry simulations."""

from asteroid_entry.conditions import EntryConditions
from asteroid_entry.model import EntryModel
from asteroid_entry.options import SolverOptions
from asteroid_entry.result import SimulationResult


def simulate_entry(
    conditions: EntryConditions,
    *,
    model: EntryModel | None = None,
    options: SolverOptions | None = None,
) -> SimulationResult:
    """Simulate the atmospheric entry of an asteroid."""
    raise NotImplementedError
