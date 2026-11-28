"""Tests for analytical and empirical atmospheric density models."""

from math import e, isfinite

import pytest

from asteroid_entry.atmosphere import (
    Atmosphere,
    ConstantAtmosphere,
    ExponentialAtmosphere,
    GlennAtmosphere,
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

    @pytest.mark.parametrize(
        "surface_density",
        [-1.0, float("nan"), float("inf"), -float("inf")],
        ids=["negative", "nan", "positive-infinity", "negative-infinity"],
    )
    def test_invalid_surface_density(self, surface_density: float) -> None:
        """Verify that invalid surface density values are rejected.

        Parameters
        ----------
        surface_density : float
            Invalid prescribed atmospheric mass density (kg m^-3).

        Notes
        -----
        Atmospheric mass density must be finite and non-negative.
        A surface density of zero remains valid and represents a
        vacuum.

        Validation is expected to occur during model initialization
        rather than during subsequent density evaluations.
        """
        with pytest.raises(ValueError):
            ConstantAtmosphere(surface_density=surface_density)


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

    @pytest.mark.parametrize(
        "surface_density",
        [-1.0, float("nan"), float("inf"), -float("inf")],
        ids=["negative", "nan", "positive-infinity", "negative-infinity"],
    )
    def test_invalid_surface_density(self, surface_density: float) -> None:
        """Verify that invalid surface density values are rejected.

        Parameters
        ----------
        surface_density : float
            Invalid atmospheric mass density at zero altitude
            (kg m^-3).

        Notes
        -----
        The surface density must be finite and non-negative.
        A surface density of zero remains valid and represents a
        vacuum.

        Validation is expected to occur during model initialization.
        """
        with pytest.raises(ValueError):
            ExponentialAtmosphere(surface_density=surface_density)

    @pytest.mark.parametrize(
        "scale_height",
        [0.0, -1.0, float("nan"), float("inf"), -float("inf")],
        ids=[
            "zero",
            "negative",
            "nan",
            "positive-infinity",
            "negative-infinity",
        ],
    )
    def test_invalid_scale_height(self, scale_height: float) -> None:
        r"""Verify that invalid atmospheric scale heights are rejected.

        Parameters
        ----------
        scale_height : float
            Invalid atmospheric density scale height (m).

        Notes
        -----
        The exponential atmospheric density model is defined by

        .. math::

            \rho_a(z) = \rho_0 \exp\left(-\frac{z}{H}\right),

        where :math:`\rho_a` is the atmospheric mass density,
        :math:`\rho_0` is the surface density, :math:`z` is the
        geometric altitude and :math:`H` is the density scale height.

        A zero scale height makes the expression undefined, whereas
        a negative scale height produces increasing density with
        increasing altitude for positive surface density.

        The scale height must therefore be finite and strictly
        positive for the intended physical model. Validation is
        expected to occur during model initialization.
        """
        with pytest.raises(ValueError):
            ExponentialAtmosphere(scale_height=scale_height)


class TestGlennAtmosphere:
    """Tests for the NASA Glenn empirical atmospheric density model."""

    # Reference densities evaluated using the original temperature
    # and pressure fits in degrees Celsius and kilopascals.
    @pytest.mark.parametrize(
        ("altitude", "expected_density"),
        [
            (0.0, 1.22661378741097),
            (5_000.0, 0.737674576847043),
            (20_000.0, 0.0889700411864835),
            (50_000.0, 1.01551513243895e-3),
            (80_000.0, 3.65450834776723e-5),
            (100_000.0, 6.00668923433141e-6),
        ],
    )
    def test_reference_density(self, altitude: float, expected_density: float) -> None:
        """Verify atmospheric density against reference calculations.

        Parameters
        ----------
        altitude : float
            Geometric altitude relative to the Earth's reference
            surface (m).
        expected_density : float
            Reference atmospheric mass density (kg m^-3).

        Notes
        -----
        The reference values are calculated using the original empirical
        expressions rather than the reformulated SI implementation.

        Agreement verifies consistency with the original formulation,
        not agreement with measured atmospheric densities.
        """
        assert GlennAtmosphere().density(altitude) == pytest.approx(
            expected_density, rel=1e-10, abs=0.0
        )

    @pytest.mark.parametrize(
        ("altitude", "expected_density"),
        [
            (10_999.0, 0.365201392145206),
            (11_000.0, 0.365512214480260),
            (11_001.0, 0.365454833567106),
            (24_999.0, 0.0405873603692201),
            (25_000.0, 0.0399455056776541),
            (25_001.0, 0.0399386766080643),
        ],
    )
    def test_layer_boundaries(self, altitude: float, expected_density: float) -> None:
        """Verify density evaluations at atmospheric layer boundaries.

        Parameters
        ----------
        altitude : float
            Geometric altitude at or adjacent to an atmospheric layer
            boundary (m).
        expected_density : float
            Reference atmospheric mass density (kg m^-3).

        Notes
        -----
        Evaluations are performed at each boundary and one metre above
        and below it to verify the selection of the empirical expressions.

        The independently fitted expressions are not necessarily
        continuous across the layer boundaries. These tests verify the
        expected piecewise behaviour rather than enforce continuity.
        """
        assert GlennAtmosphere().density(altitude) == pytest.approx(
            expected_density, rel=1e-10, abs=0.0
        )

    @pytest.mark.parametrize("altitude", [-8_000.0, -100.0, -1.0])
    def test_negative_altitude_clamping(self, altitude: float) -> None:
        """Verify that negative altitudes use the surface density.

        Parameters
        ----------
        altitude : float
            Negative geometric altitude relative to the Earth's
            reference surface (m).
        """
        atmosphere = GlennAtmosphere()

        assert atmosphere.density(altitude) == atmosphere.density(0.0)

    @pytest.mark.parametrize("altitude", [120_000.0, 150_000.0, 200_000.0])
    def test_high_altitude_extrapolation(self, altitude: float) -> None:
        """Verify positive, reduced density at extrapolated altitudes.

        Parameters
        ----------
        altitude : float
            Geometric altitude above the comparison altitude of
            100 km (m).

        Notes
        -----
        The uppermost empirical expression is extrapolated beyond
        the altitude range used for the reference density tests.

        This verifies mathematical behaviour at the sampled altitudes,
        not the physical validity of the high-altitude extrapolation.
        """
        atmosphere = GlennAtmosphere()
        density = atmosphere.density(altitude)

        assert 0.0 < density < atmosphere.density(100_000.0)

    @pytest.mark.parametrize("altitude", [float(z) for z in range(0, 100_001, 1_000)])
    def test_positive_finite_density(self, altitude: float) -> None:
        """Verify positive and finite density at sampled altitudes.

        Parameters
        ----------
        altitude : float
            Geometric altitude sampled between 0 and 100 km at
            intervals of 1 km (m).

        Notes
        -----
        The discrete sampling verifies positivity and finiteness at
        the selected altitudes rather than establishing these
        properties over the entire continuous altitude domain.
        """
        density = GlennAtmosphere().density(altitude)

        assert isfinite(density)
        assert density > 0.0


@pytest.mark.parametrize(
    "atmosphere",
    [ConstantAtmosphere(), ExponentialAtmosphere(), GlennAtmosphere()],
    ids=["constant", "exponential", "glenn"],
)
class TestAtmosphereContract:
    """Tests for behaviour shared by atmospheric density models."""

    @pytest.mark.parametrize("altitude", [-100.0, 0.0, 10_000.0, 100_000.0])
    def test_scalar_return_type(self, atmosphere: Atmosphere, altitude: float) -> None:
        """Verify that atmospheric density is returned as a float.

        Parameters
        ----------
        atmosphere : Atmosphere
            Atmospheric density model under test.
        altitude : float
            Geometric altitude relative to the planetary reference
            surface (m).
        """
        assert isinstance(atmosphere.density(altitude), float)

    @pytest.mark.parametrize("altitude", [-100.0, 0.0, 10_000.0, 100_000.0])
    def test_finite_non_negative_density(
        self, atmosphere: Atmosphere, altitude: float
    ) -> None:
        """Verify finite and non-negative atmospheric mass density.

        Parameters
        ----------
        atmosphere : Atmosphere
            Atmospheric density model under test.
        altitude : float
            Geometric altitude relative to the planetary reference
            surface (m).

        Notes
        -----
        Non-negative density permits vacuum configurations, whereas
        strictly positive density would exclude them.

        The test verifies the selected model configurations and
        altitudes rather than all possible model parameter values.
        """
        density = atmosphere.density(altitude)

        assert isfinite(density)
        assert density >= 0.0

    @pytest.mark.parametrize(
        "altitude",
        [float("nan"), float("inf"), -float("inf")],
        ids=["nan", "positive-infinity", "negative-infinity"],
    )
    def test_non_finite_altitude(self, atmosphere: Atmosphere, altitude: float) -> None:
        """Verify that non-finite altitude values are rejected.

        Parameters
        ----------
        atmosphere : Atmosphere
            Atmospheric density model under test.
        altitude : float
            Non-finite geometric altitude relative to the planetary
            reference surface (m).

        Notes
        -----
        Atmospheric density evaluations require a finite geometric
        altitude. Non-finite values are rejected rather than
        propagated through the atmospheric density calculations.

        Finite negative altitudes remain permitted and are handled
        according to the documented extrapolation policy of each
        atmospheric model.
        """
        with pytest.raises(ValueError):
            atmosphere.density(altitude)
