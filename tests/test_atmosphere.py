"""Tests for analytical and empirical atmospheric density models."""

from math import e

import pytest

from asteroid_entry.atmosphere import (
    ConstantAtmosphere,
    ExponentialAtmosphere,
)


class TestConstantAtmosphere:
    """Tests for the constant atmospheric density model."""

    def test_default_density(self) -> None:
        """Verify the default atmospheric mass density."""
        assert ConstantAtmosphere().density(0.0) == 1.2

    @pytest.mark.parametrize("surface_density", [0.1, 0.5, 2.0, 5.0])
    def test_custom_density(self, surface_density: float) -> None:
        """Verify that the prescribed atmospheric mass density is returned.

        Parameters
        ----------
        surface_density : float
            Prescribed atmospheric mass density (kg m^-3).
        """
        atmosphere = ConstantAtmosphere(surface_density=surface_density)

        assert atmosphere.density(0.0) == surface_density

    @pytest.mark.parametrize("altitude", [-8_000.0, 0.0, 10_000.0, 50_000.0, 100_000.0])
    def test_altitude_independence(self, altitude: float) -> None:
        """Verify that atmospheric mass density is independent of altitude.

        Parameters
        ----------
        altitude : float
            Geometric altitude relative to the planetary reference
            surface (m).
        """
        atmosphere = ConstantAtmosphere(surface_density=0.8)

        assert atmosphere.density(altitude) == 0.8

    @pytest.mark.parametrize("altitude", [-1_000.0, 0.0, 100_000.0])
    def test_vacuum(self, altitude: float) -> None:
        """Verify that the vacuum configuration returns zero density.

        Parameters
        ----------
        altitude : float
            Geometric altitude relative to the planetary reference
            surface (m).
        """
        atmosphere = ConstantAtmosphere(surface_density=0.0)

        assert atmosphere.density(altitude) == 0.0


class TestExponentialAtmosphere:
    """Tests for the exponential atmospheric density model."""

    def test_default_surface_density(self) -> None:
        """Verify the default atmospheric mass density at zero altitude."""
        assert ExponentialAtmosphere().density(0.0) == 1.2

    @pytest.mark.parametrize("surface_density", [0.5, 2.0, 5.0])
    def test_custom_surface_density(self, surface_density: float) -> None:
        """Verify the prescribed atmospheric mass density at zero altitude.

        Parameters
        ----------
        surface_density : float
            Prescribed atmospheric mass density at zero altitude
            (kg m^-3).
        """
        atmosphere = ExponentialAtmosphere(surface_density=surface_density)

        assert atmosphere.density(0.0) == surface_density

    @pytest.mark.parametrize("multiple", [1, 2, 3, 5])
    def test_density_at_scale_height_multiples(self, multiple: int) -> None:
        r"""Verify density at integer multiples of the scale height.

        Parameters
        ----------
        multiple : int
            Positive integer multiple of the atmospheric density scale
            height.

        Notes
        -----
        At an altitude :math:`z = nH`, the analytical solution is

        .. math::

            \rho_a(nH) = \rho_0 e^{-n},

        where :math:`n` is the integer multiple, :math:`H` is the
        density scale height, :math:`z` is the geometric altitude,
        :math:`\rho_a` is the atmospheric mass density and
        :math:`\rho_0` is the surface density.
        """
        atmosphere = ExponentialAtmosphere()

        assert atmosphere.density(multiple * 8_000.0) == pytest.approx(
            1.2 / e**multiple, rel=1e-12, abs=0.0
        )

    @pytest.mark.parametrize("scale_height", [4_000.0, 10_000.0, 20_000.0])
    def test_custom_scale_height(self, scale_height: float) -> None:
        r"""Verify the density evaluated at a prescribed scale height.

        Parameters
        ----------
        scale_height : float
            Prescribed atmospheric density scale height (m).

        Notes
        -----
        At one scale height, the atmospheric mass density is

        .. math::

            \rho_a(H) = \frac{\rho_0}{e},

        independently of the prescribed scale height.
        """
        atmosphere = ExponentialAtmosphere(
            surface_density=2.0, scale_height=scale_height
        )

        assert atmosphere.density(scale_height) == pytest.approx(
            2.0 / e, rel=1e-12, abs=0.0
        )

    def test_monotonic_decay(self) -> None:
        """Verify strictly decreasing density at sampled altitudes."""
        atmosphere = ExponentialAtmosphere()
        altitudes = [0.0, 8_000.0, 20_000.0, 50_000.0, 100_000.0]
        densities = [atmosphere.density(z) for z in altitudes]

        assert all(a > b for a, b in zip(densities[:-1], densities[1:], strict=True))

    @pytest.mark.parametrize("multiple", [1, 2])
    def test_negative_altitude_extrapolation(self, multiple: int) -> None:
        r"""Verify analytical density extrapolation below zero altitude.

        Parameters
        ----------
        multiple : int
            Positive integer multiple of the atmospheric density scale
            height, evaluated below the reference surface.

        Notes
        -----
        At a negative altitude :math:`z = -nH`, the extrapolated
        atmospheric mass density is

        .. math::

            \rho_a(-nH) = \rho_0 e^n.

        This verifies mathematical extrapolation rather than physical
        validity below the planetary reference surface.
        """
        atmosphere = ExponentialAtmosphere()

        assert atmosphere.density(-multiple * 8_000.0) == pytest.approx(
            1.2 * e**multiple, rel=1e-12, abs=0.0
        )

    def test_high_altitude_decay(self) -> None:
        """Verify a small but positive density at a high altitude."""
        atmosphere = ExponentialAtmosphere()

        assert 0.0 < atmosphere.density(800_000.0) < 1e-40

    @pytest.mark.parametrize("altitude", [-8_000.0, 0.0, 100_000.0])
    def test_vacuum(self, altitude: float) -> None:
        """Verify that the vacuum configuration returns zero density.

        Parameters
        ----------
        altitude : float
            Geometric altitude relative to the planetary reference
            surface (m).
        """
        atmosphere = ExponentialAtmosphere(surface_density=0.0)

        assert atmosphere.density(altitude) == 0.0
