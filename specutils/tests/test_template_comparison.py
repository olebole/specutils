import astropy.units as u
import numpy as np
from astropy.nddata import StdDevUncertainty

from ..spectra.spectrum1d import Spectrum1D
from ..spectra.spectrum_collection import SpectrumCollection
from ..analysis import template_comparison
from astropy.tests.helper import quantity_allclose


def test_template_match_no_overlap():
    """
    Test template_match when both observed and template spectra have no overlap on the wavelength axis.
    """
    # Seed np.random so that results are consistent
    np.random.seed(42)

    # Create test spectra
    spec_axis = np.linspace(0, 50, 50) * u.AA
    spec_axis_no_overlap = np.linspace(51, 102, 50) * u.AA

    spec = Spectrum1D(spectral_axis=spec_axis,
                      flux=np.random.randn(50) * u.Jy,
                      uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    spec1 = Spectrum1D(spectral_axis=spec_axis_no_overlap,
                       flux=np.random.randn(50) * u.Jy,
                       uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Get result from template_match
    tm_result = template_comparison.template_match(spec, spec1)

    # Create new spectrum for comparison
    spec_result = Spectrum1D(spectral_axis=spec_axis,
                             flux=spec1.flux * template_comparison._normalize_for_template_matching(spec, spec1))

    # assert quantity_allclose(tm_result[0].flux, spec_result.flux, atol=0.01*u.Jy)
    assert np.isnan(tm_result[1])

def test_template_match_minimal_overlap():
    """
    Test template_match when both observed and template spectra have minimal overlap on the wavelength axis.
    """
    # Seed np.random so that results are consistent
    np.random.seed(42)

    # Create test spectra
    spec_axis = np.linspace(0, 50, 50) * u.AA
    spec_axis_min_overlap = np.linspace(50, 100, 50) * u.AA

    spec_axis[49] = 51.0 * u.AA
    spec_axis_min_overlap[0] = 51.0 * u.AA

    spec = Spectrum1D(spectral_axis=spec_axis,
                      flux=np.random.randn(50) * u.Jy,
                      uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    spec1 = Spectrum1D(spectral_axis=spec_axis_min_overlap,
                       flux=np.random.randn(50) * u.Jy,
                       uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Get result from template_match
    tm_result = template_comparison.template_match(spec, spec1)

    # Create new spectrum for comparison
    spec_result = Spectrum1D(spectral_axis=spec_axis,
                             flux=spec1.flux * template_comparison._normalize_for_template_matching(spec, spec1))

    # assert quantity_allclose(tm_result[0].flux, spec_result.flux, atol=0.01*u.Jy)
    # TODO: investigate why the all elements in tm_result[1] are NaN even with overlap
    assert np.isnan(tm_result[1])

def test_template_match_spectrum():
    """
    Test template_match when both observed and template spectra have the same wavelength axis.
    """
    # Seed np.random so that results are consistent
    np.random.seed(42)

    # Create test spectra
    spec_axis = np.linspace(0, 50, 50) * u.AA
    spec = Spectrum1D(spectral_axis=spec_axis,
                      flux=np.random.randn(50) * u.Jy,
                      uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    spec1 = Spectrum1D(spectral_axis=spec_axis,
                       flux=np.random.randn(50) * u.Jy,
                       uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Get result from template_match
    tm_result = template_comparison.template_match(spec, spec1)

    # Create new spectrum for comparison
    spec_result = Spectrum1D(spectral_axis=spec_axis,
                             flux=spec1.flux * template_comparison._normalize_for_template_matching(spec, spec1))

    assert quantity_allclose(tm_result[0].flux, spec_result.flux, atol=0.01*u.Jy)
    assert tm_result[1] == 40093.28353756253


def test_template_match_with_resample():
    """
    Test template_match when both observed and template spectra have different wavelength axis using resampling.
    """
    np.random.seed(42)

    # Create test spectra
    spec_axis1 = np.linspace(0, 50, 50) * u.AA
    spec_axis2 = np.linspace(0, 50, 50) * u.AA
    spec = Spectrum1D(spectral_axis=spec_axis1,
                      flux=np.random.randn(50) * u.Jy,
                      uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    spec1 = Spectrum1D(spectral_axis=spec_axis2,
                       flux=np.random.randn(50) * u.Jy,
                       uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Get result from template_match
    tm_result = template_comparison.template_match(spec, spec1)

    # Create new spectrum for comparison
    spec_result = Spectrum1D(spectral_axis=spec_axis1,
                             flux=spec1.flux * template_comparison._normalize_for_template_matching(spec, spec1))

    assert quantity_allclose(tm_result[0].flux, spec_result.flux, atol=0.01*u.Jy)
    np.testing.assert_almost_equal(tm_result[1], 40093.28353756253)


def test_template_match_list():
    """
    Test template_match when template spectra are in a list.
    """
    np.random.seed(42)

    # Create test spectra
    spec_axis1 = np.linspace(0, 50, 50) * u.AA
    spec_axis2 = np.linspace(0, 50, 50) * u.AA
    spec = Spectrum1D(spectral_axis=spec_axis1,
                      flux=np.random.randn(50) * u.Jy,
                      uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    spec1 = Spectrum1D(spectral_axis=spec_axis2,
                       flux=np.random.randn(50) * u.Jy,
                       uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))
    spec2 = Spectrum1D(spectral_axis=spec_axis2,
                       flux=np.random.randn(50) * u.Jy,
                       uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Combine spectra into list
    template_list = [spec1, spec2]

    # Get result from template_match
    tm_result = template_comparison.template_match(spec, template_list)

    np.testing.assert_almost_equal(tm_result[1], 40093.28353756253)

    # make sure that multiple template spectra will create a list of
    # chi2 values, one per template.
    assert len(tm_result) == 4


def test_template_match_spectrum_collection():
    """
    Test template_match when template spectra are in a SpectrumCollection object.
    """
    np.random.seed(42)

    # Create test spectra
    spec_axis1 = np.linspace(0, 50, 50) * u.AA
    spec_axis2 = np.linspace(0, 50, 50) * u.AA
    spec = Spectrum1D(spectral_axis=spec_axis1,
                      flux=np.random.randn(50) * u.Jy,
                      uncertainty=StdDevUncertainty(np.random.sample(50)))
    spec1 = Spectrum1D(spectral_axis=spec_axis2,
                       flux=np.random.randn(50) * u.Jy,
                       uncertainty=StdDevUncertainty(np.random.sample(50)))
    spec2 = Spectrum1D(spectral_axis=spec_axis2,
                       flux=np.random.randn(50) * u.Jy,
                       uncertainty=StdDevUncertainty(np.random.sample(50)))

    # Combine spectra into SpectrumCollection object
    spec_coll = SpectrumCollection.from_spectra([spec1, spec2])

    # Get result from template_match
    tm_result = template_comparison.template_match(spec, spec_coll)

    np.testing.assert_almost_equal(tm_result[1], 40093.28353756253)


def test_template_match_multidim_spectrum():
    """
    Test template matching with a multi-dimensional Spectrum1D object.
    """
    np.random.seed(42)

    # Create test spectra
    spec_axis1 = np.linspace(0, 50, 50) * u.AA
    spec_axis2 = np.linspace(0, 50, 50) * u.AA

    spec = Spectrum1D(spectral_axis=spec_axis1,
                      flux=np.random.sample(50) * u.Jy,
                      uncertainty=StdDevUncertainty(np.random.sample(50)))
    multidim_spec = Spectrum1D(spectral_axis=spec_axis2,
                               flux=np.random.sample((2, 50)) * u.Jy,
                               uncertainty=StdDevUncertainty(np.random.sample((2, 50))))

    # Get result from template_match
    tm_result = template_comparison.template_match(spec, multidim_spec)

    np.testing.assert_almost_equal(tm_result[1], 250.26870401777543)

def test_template_unknown_redshift():
    """
    Test template redshift when redshift is unknown.
    """
    # Seed np.random so that results are consistent
    np.random.seed(42)

    # Create test spectra
    spec_axis = np.linspace(0, 50, 50) * u.AA
    perm_flux = np.random.randn(50) * u.Jy

    redshift = 3

    # Observed spectrum
    spec = Spectrum1D(spectral_axis=spec_axis * (1+redshift),
                      flux=perm_flux,
                      uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Template spectrum
    spec1 = Spectrum1D(spectral_axis=spec_axis,
                       flux=perm_flux,
                       uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Test redshift parameters
    min_redshift = .5
    max_redshift = 5.5
    delta_redshift = .25
    redshift_trial_values = np.arange(min_redshift, max_redshift, delta_redshift)

    tr_result = template_comparison.template_redshift(observed_spectrum=spec, template_spectrum=spec1,
                                                      redshift=redshift_trial_values)

    assert len(tr_result) == 3
    assert tr_result[0] == 3

def test_template_redshift_with_one_template_spectrum_in_match():
    # Seed np.random so that results are consistent
    np.random.seed(42)

    # Create test spectra
    spec_axis = np.linspace(0, 50, 50) * u.AA
    perm_flux = np.random.randn(50) * u.Jy

    # Test redshift
    redshift = 3

    # Observed spectrum
    spec = Spectrum1D(spectral_axis=spec_axis * (1+redshift),
                      flux=perm_flux,
                      uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Template spectrum
    spec1 = Spectrum1D(spectral_axis=spec_axis,
                       flux=perm_flux,
                       uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Test redshift parameters
    min_redshift = .5
    max_redshift = 5.5
    delta_redshift = .25
    redshift_trial_values = np.arange(min_redshift, max_redshift+delta_redshift, delta_redshift)

    tm_result = template_comparison.template_match(observed_spectrum=spec, spectral_templates=spec1,
                                                      resample_method="flux_conserving", known_redshift=None,
                                                      redshift=redshift_trial_values)

    np.testing.assert_almost_equal(tm_result[1], 73484.0053895151)

def test_template_redshift_with_multiple_template_spectra_in_match():
    # Seed np.random so that results are consistent
    np.random.seed(42)

    # Create test spectra
    spec_axis = np.linspace(0, 50, 50) * u.AA
    perm_flux = np.random.randn(50) * u.Jy

    # Test redshift
    redshift = 3

    # Observed spectrum
    spec = Spectrum1D(spectral_axis=spec_axis * (1+redshift),
                      flux=perm_flux,
                      uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Template spectrum
    spec1 = Spectrum1D(spectral_axis=spec_axis,
                       flux=np.random.randn(50) * u.Jy,
                       uncertainty=StdDevUncertainty(np.random.sample(50)))
    spec2 = Spectrum1D(spectral_axis=spec_axis,
                       flux=np.random.randn(50) * u.Jy,
                       uncertainty=StdDevUncertainty(np.random.sample(50)))

    # Combine spectra into SpectrumCollection object
    spec_coll = SpectrumCollection.from_spectra([spec1, spec2])

    # Test redshift parameters
    min_redshift = .5
    max_redshift = 5.5
    delta_redshift = .25
    redshift_trial_values = np.arange(min_redshift, max_redshift+delta_redshift, delta_redshift)

    tm_result = template_comparison.template_match(observed_spectrum=spec, spectral_templates=spec_coll,
                                                      resample_method="flux_conserving", known_redshift=None,
                                                      redshift=redshift_trial_values)

    np.testing.assert_almost_equal(tm_result[1], 6803.922741644725)

def test_template_known_redshift():
    """
    Test template match when the redshift is known.
    """
    # Seed np.random so that results are consistent
    np.random.seed(42)

    # Create test spectra
    spec_axis = np.linspace(0, 50, 50) * u.AA
    perm_flux = np.random.randn(50) * u.Jy

    redshift = 3

    # Observed spectrum
    spec = Spectrum1D(spectral_axis=spec_axis * (1+redshift),
                      flux=perm_flux,
                      uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    # Template spectrum
    spec1 = Spectrum1D(spectral_axis=spec_axis,
                       flux=perm_flux,
                       uncertainty=StdDevUncertainty(np.random.sample(50), unit='Jy'))

    tm_result = template_comparison.template_match(observed_spectrum=spec, spectral_templates=spec1,
                                                      resample_method="flux_conserving", known_redshift=redshift,
                                                      redshift=None)
    np.testing.assert_almost_equal(tm_result[1], 1.9062409482056814e-31)
