from unittest.mock import patch

from core.helpers import CacheControlMixin, YNRAPIHelper
from django.http import HttpResponse
from django.views import View


def test_ynr_get(settings):
    settings.YNR_BASE_URL = "https://example.com/"
    ynr_api_key = "test_api_key"
    endpoint = "ballots"
    expected_url = "https://example.com/api/next/ballots"
    expected_params = {"auth_token": ynr_api_key}

    api_helper = YNRAPIHelper(api_key=ynr_api_key)

    with patch("core.helpers.session.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"results": []}

        result = api_helper.get(endpoint)

        mock_get.assert_called_once_with(expected_url, params=expected_params)
        assert result == {"results": []}


def test_cache_control_mixin(settings, rf):
    class TestView(CacheControlMixin, View):
        cache_timeout = 123

        def get(self, request):
            return HttpResponse("")

    test_view = TestView.as_view()

    settings.DEBUG = False
    request = rf.get("/")
    assert test_view(request).headers["Cache-Control"] == "max-age=123"

    settings.DEBUG = True
    request = rf.get("/")
    assert (
        test_view(request).headers["Cache-Control"]
        == "max-age=0, no-cache, no-store, must-revalidate, private"
    )
