"""Smoke tests for the installed package."""

import asteroid_entry


def test_package_import() -> None:
    """Verify that the installed package can be imported."""
    assert asteroid_entry.__file__ is not None
