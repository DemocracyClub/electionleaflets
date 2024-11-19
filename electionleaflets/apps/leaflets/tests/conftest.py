from unittest.mock import patch

import pytest



@pytest.fixture
def mock_get_ballot_data_from_ynr():
    def _mock_ynr_value(return_value):
        return patch(
            "leaflets.forms.PartyForm.get_ballot_data_from_ynr",
            return_value=return_value
        )
    return _mock_ynr_value
