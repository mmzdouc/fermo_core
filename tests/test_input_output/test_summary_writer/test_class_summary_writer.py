import os
from pathlib import Path

import pytest

from fermo_core.input_output.class_summary_writer import SummaryWriter
from fermo_core.input_output.class_validation_manager import ValidationManager


@pytest.fixture
def summary_writer(parameter_instance):
    return SummaryWriter(
        params=parameter_instance,
        destination=Path("tests/test_input_output/test_summary_writer/summary.txt"),
    )


def test_write_summary(summary_writer):
    summary_writer.summary.append("Test")
    summary_writer.write_summary()
    assert ValidationManager.validate_file_exists(summary_writer.destination) is None
    os.remove(summary_writer.destination)


def test_summarize_peaktableparameters_valid(summary_writer):
    summary_writer.summarize_peaktableparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_peaktableparameters_invalid(summary_writer):
    summary_writer.params.PeaktableParameters = None
    summary_writer.summarize_peaktableparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_msmsparameters_valid(summary_writer):
    summary_writer.summarize_msmsparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_msmsparameters_invalid(summary_writer):
    summary_writer.params.MsmsParameters = None
    summary_writer.summarize_msmsparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_phenotypeparameters_valid(summary_writer):
    summary_writer.summarize_phenotypeparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_phenotypeparameters_invalid(summary_writer):
    summary_writer.params.PhenotypeParameters = None
    summary_writer.summarize_phenotypeparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_groupmetadataparameters_valid(summary_writer):
    summary_writer.summarize_groupmetadataparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_groupmetadataparameters_invalid(summary_writer):
    summary_writer.params.GroupMetadataParameters = None
    summary_writer.summarize_groupmetadataparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_speclibparameters_valid(summary_writer):
    summary_writer.summarize_speclibparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_speclibparameters_invalid(summary_writer):
    summary_writer.params.SpecLibParameters = None
    summary_writer.summarize_speclibparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_ms2queryresultsparameters_valid(summary_writer):
    summary_writer.summarize_ms2queryresultsparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_ms2queryresultsparameters_invalid(summary_writer):
    summary_writer.params.MS2QueryResultsParameters = None
    summary_writer.summarize_ms2queryresultsparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_asresultsparameters_valid(summary_writer):
    summary_writer.summarize_asresultsparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_asresultsparameters_invalid(summary_writer):
    summary_writer.params.AsResultsParameters = None
    summary_writer.summarize_asresultsparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_featurefilteringparameters_valid(summary_writer):
    summary_writer.summarize_featurefilteringparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_featurefilteringparameters_invalid(summary_writer):
    summary_writer.params.FeatureFilteringParameters.activate_module = False
    summary_writer.summarize_featurefilteringparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_adductannotationparameters_valid(summary_writer):
    summary_writer.summarize_adductannotationparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_adductannotationparameters_invalid(summary_writer):
    summary_writer.params.AdductAnnotationParameters.activate_module = False
    summary_writer.summarize_adductannotationparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_neutrallossparameters_valid(summary_writer):
    summary_writer.summarize_neutrallossparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_neutrallossparameters_invalid(summary_writer):
    summary_writer.params.NeutralLossParameters.activate_module = False
    summary_writer.summarize_neutrallossparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_fragmentannparameters_valid(summary_writer):
    summary_writer.summarize_fragmentannparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_fragmentannparameters_invalid(summary_writer):
    summary_writer.params.FragmentAnnParameters.activate_module = False
    summary_writer.summarize_fragmentannparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_specsimnetworkcosineparameters_valid(summary_writer):
    summary_writer.summarize_specsimnetworkcosineparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_specsimnetworkcosineparameters_invalid(summary_writer):
    summary_writer.params.SpecSimNetworkCosineParameters.activate_module = False
    summary_writer.summarize_specsimnetworkcosineparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_specsimnetworkdeepscoreparameters_valid(summary_writer):
    summary_writer.summarize_specsimnetworkdeepscoreparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_specsimnetworkdeepscoreparameters_invalid(summary_writer):
    summary_writer.params.SpecSimNetworkDeepscoreParameters.activate_module = False
    summary_writer.summarize_specsimnetworkdeepscoreparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_blankassignmentparameters_valid(summary_writer):
    summary_writer.summarize_blankassignmentparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_blankassignmentparameters_invalid(summary_writer):
    summary_writer.params.BlankAssignmentParameters.activate_module = False
    summary_writer.summarize_blankassignmentparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_groupfactassignmentparameters_valid(summary_writer):
    summary_writer.summarize_groupfactassignmentparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_groupfactassignmentparameters_invalid(summary_writer):
    summary_writer.params.GroupFactAssignmentParameters.activate_module = False
    summary_writer.summarize_groupfactassignmentparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_phenoqualassgnparams_valid(summary_writer):
    summary_writer.summarize_phenoqualassgnparams()
    assert len(summary_writer.summary) != 0


def test_summarize_phenoqualassgnparams_invalid(summary_writer):
    summary_writer.params.PhenoQualAssgnParams.activate_module = False
    summary_writer.summarize_phenoqualassgnparams()
    assert len(summary_writer.summary) == 0


def test_summarize_phenoquantpercentassgnparams_valid(summary_writer):
    summary_writer.params.PhenoQuantPercentAssgnParams.activate_module = True
    summary_writer.summarize_phenoquantpercentassgnparams()
    assert len(summary_writer.summary) != 0


def test_summarize_phenoquantpercentassgnparams_invalid(summary_writer):
    summary_writer.params.PhenoQuantPercentAssgnParams.activate_module = False
    summary_writer.summarize_phenoquantpercentassgnparams()
    assert len(summary_writer.summary) == 0


def test_summarize_phenoquantconcassgnparams_valid(summary_writer):
    summary_writer.params.PhenoQuantConcAssgnParams.activate_module = True
    summary_writer.summarize_phenoquantconcassgnparams()
    assert len(summary_writer.summary) != 0


def test_summarize_phenoquantconcassgnparams_invalid(summary_writer):
    summary_writer.params.PhenoQuantConcAssgnParams.activate_module = False
    summary_writer.summarize_phenoquantconcassgnparams()
    assert len(summary_writer.summary) == 0


def test_summarize_spectrallibmatchingcosineparameters_valid(summary_writer):
    summary_writer.params.SpectralLibMatchingCosineParameters.activate_module = True
    summary_writer.summarize_spectrallibmatchingcosineparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_spectrallibmatchingcosineparameters_invalid(summary_writer):
    summary_writer.params.SpectralLibMatchingCosineParameters.activate_module = False
    summary_writer.summarize_spectrallibmatchingcosineparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_spectrallibmatchingdeepscoreparameters_valid(summary_writer):
    summary_writer.params.SpectralLibMatchingDeepscoreParameters.activate_module = True
    summary_writer.summarize_spectrallibmatchingdeepscoreparameters()
    assert len(summary_writer.summary) != 0


def test_summarize_spectrallibmatchingdeepscoreparameters_invalid(summary_writer):
    summary_writer.params.SpectralLibMatchingDeepscoreParameters.activate_module = False
    summary_writer.summarize_spectrallibmatchingdeepscoreparameters()
    assert len(summary_writer.summary) == 0


def test_summarize_askcbcosinematchingparams_valid(summary_writer):
    summary_writer.params.AsKcbCosineMatchingParams.activate_module = True
    summary_writer.summarize_askcbcosinematchingparams()
    assert len(summary_writer.summary) != 0


def test_summarize_askcbcosinematchingparams_invalid(summary_writer):
    summary_writer.params.AsKcbCosineMatchingParams.activate_module = False
    summary_writer.summarize_askcbcosinematchingparams()
    assert len(summary_writer.summary) == 0


def test_summarize_askcbdeepscorematchingparams_valid(summary_writer):
    summary_writer.params.AsKcbDeepscoreMatchingParams.activate_module = True
    summary_writer.summarize_askcbdeepscorematchingparams()
    assert len(summary_writer.summary) != 0


def test_summarize_askcbdeepscorematchingparams_invalid(summary_writer):
    summary_writer.params.AsKcbDeepscoreMatchingParams.activate_module = False
    summary_writer.summarize_askcbdeepscorematchingparams()
    assert len(summary_writer.summary) == 0
