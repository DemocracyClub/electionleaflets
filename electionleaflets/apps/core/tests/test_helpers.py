from unittest.mock import patch

from core.helpers import YNRAPIHelper


def test_ynr_get(settings):
    settings.YNR_BASE_URL = "https://example.com/"
    ynr_api_key = "test_api_key"
    endpoint = "ballots"
    expected_url = "https://example.com/api/next/ballots"
    expected_params = {"auth_token": ynr_api_key}

    api_helper = YNRAPIHelper(api_key=ynr_api_key)

    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"results": []}

        result = api_helper.get(endpoint)

        mock_get.assert_called_once_with(expected_url, params=expected_params)
        assert result == {"results": []}
