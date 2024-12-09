import pytest
from constituencies.models import Constituency
from elections.models import Election


@pytest.fixture
def constituency():
    return Constituency.objects.create(name="Test Constituency")


@pytest.fixture
def election():
    return Election.objects.create(
        name="Test Election", live_date="2023-01-01", dead_date="2023-01-01"
    )
