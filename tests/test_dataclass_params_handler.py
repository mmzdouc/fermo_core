from pathlib import Path

import pytest
from fermo_core.input_output.dataclass_params_handler import ParamsHandler


@pytest.fixture
def params_handler():
    return ParamsHandler("0.1.0", Path("my/path/here"))


def test_default_values_class_params_handler(params_handler):
    for a in dir(params_handler):
        if not a.startswith("_"):
            if a == "version":
                assert getattr(params_handler, a) == "0.1.0"
            elif a == "root":
                assert getattr(params_handler, a) == Path("my/path/here")
            elif a == "session":
                assert getattr(params_handler, a) is None
            elif a == "peaktable_mzmine3":
                assert getattr(params_handler, a) is None
            elif a == "phenotype_fermo_mode":
                assert getattr(params_handler, a) is None
            elif a == "msms_mgf":
                assert getattr(params_handler, a) is None
            elif a == "phenotype_fermo":
                assert getattr(params_handler, a) is None
            elif a == "group_fermo":
                assert getattr(params_handler, a) is None
            elif a == "speclib_mgf":
                assert getattr(params_handler, a) is None
            elif a == "mass_dev_ppm":
                assert getattr(params_handler, a) == 20
            elif a == "msms_frag_min":
                assert getattr(params_handler, a) == 5
            elif a == "phenotype_fold":
                assert getattr(params_handler, a) == 10
            elif a == "column_ret_fold":
                assert getattr(params_handler, a) == 10
            elif a == "fragment_tol":
                assert getattr(params_handler, a) == 0.1
            elif a == "spectral_sim_score_cutoff":
                assert getattr(params_handler, a) == 0.7
            elif a == "max_nr_links_spec_sim":
                assert getattr(params_handler, a) == 10
            elif a == "min_nr_matched_peaks":
                assert getattr(params_handler, a) == 5
            elif a == "spectral_sim_network_alg":
                assert getattr(params_handler, a) == "modified_cosine"
            elif a == "flag_ms2query":
                assert getattr(params_handler, a) is False
            elif a == "flag_ms2query_blank":
                assert getattr(params_handler, a) is False
            elif a == "ms2query_filter_range":
                assert getattr(params_handler, a) == (0.0, 1.0)
            elif a == "rel_int_range":
                assert getattr(params_handler, a) == (0.0, 1.0)
            else:
                assert False, f"{a} is not covered by this unit test."
