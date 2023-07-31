from fermo_core.input_output.class_comm_line_handler import CommLineHandler
from fermo_core.input_output.class_params_handler import ParamsHandler


def test_success_validate_input_arg():
    comm_line_handler = CommLineHandler()
    params = ParamsHandler
    assert comm_line_handler.validate_input_arg(
        getattr(params, "validate_string"), "string", "param_name"
    )
