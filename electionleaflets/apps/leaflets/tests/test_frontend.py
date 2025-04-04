from pathlib import Path
from urllib.parse import urljoin

import pytest
from django.urls import reverse
from leaflets.models import Leaflet, LeafletImage
from leaflets.tests.data import LOCAL_BALLOT_WITH_CANDIDATES
from leaflets.tests.model_factory import LeafletFactory
from playwright.sync_api import Page, expect

from electionleaflets import settings


def console_handler(message):
    """
    Called when the console receives a message, and raises the message unless
    it's a content warning. We don't mind about 3rd party package warnings
    as they're typically an artifact of the test server rather than an actual
    error.

    We also ignore any 3rd party assets that can't be loaded because the
    test environment isn't connected to the internet.

    """
    if "Third-party cookie will be blocked" in message.text:
        return
    if "net::ERR_INTERNET_DISCONNECTED" in message.text:
        return
    assert not message.text, (
        f"Found browser console output: {message.text}: {message.location}"
    )


class TestLeafletUpload:
    @pytest.fixture(autouse=True)
    def setup_method(
        self, page: Page, live_server, mock_get_ballot_data_from_ynr
    ):
        self.page = page
        # Raise if the console contains errors
        self.page.on("console", console_handler)
        self.live_server = live_server
        self.mock_get_ballot_data_from_ynr = mock_get_ballot_data_from_ynr

    def navigate_to_home_page(self):
        self.page.goto(self.live_server.url)

    def get_test_image(self, leaflet_file_path="front_test.jpg"):
        project_root = Path(settings.PROJECT_ROOT).resolve()
        return [
            str(
                project_root
                / "apps/leaflets/tests/test_images"
                / leaflet_file_path
            )
        ]

    def navigate_to_upload_page(self):
        upload_link = self.page.get_by_role("link", name="Upload a leaflet")
        upload_link.click()
        expect(self.page).to_have_url(
            f"{self.live_server.url}/leaflets/add/images/"
        )
        take_photo_link = self.page.get_by_label("Take a photo of a leaflet")
        take_photo_link.click()

    def upload_leaflet(self, files=None):
        if not files:
            files = self.get_test_image()
        self.navigate_to_home_page()
        self.navigate_to_upload_page()

        self.page.set_input_files(selector='input[type="file"]', files=files)
        submit_button = self.page.get_by_role("button", name="Continue")
        submit_button.click()

    def upload_multiple_files_for_one_leaflet(self):
        self.navigate_to_home_page()
        self.navigate_to_upload_page()
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_text("Take a photo of a leaflet").click()
        file_chooser = fc_info.value
        file_chooser.set_files(self.get_test_image())

        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_text("Add another image of this").click()
        file_chooser = fc_info.value
        file_chooser.set_files(self.get_test_image("back_test.jpg"))

        # Ensure the JS has finished processing before continuing
        self.page.wait_for_timeout(500)
        self.page.get_by_role("button", name="Continue").click()

    def fill_postcode(self, postcode="SW1A 1AA"):
        postcode_input = self.page.get_by_label("What postcode was this")
        postcode_input.click()
        postcode_input.fill(postcode)

    def select_time_and_submit(self):
        time_input = self.page.get_by_text("In the last couple of weeks")
        time_input.check()
        submit_button = self.page.get_by_role("button", name="Submit")
        submit_button.click()

    def select_party_and_submit(self, party="Green Party"):
        party_option = self.page.get_by_text(party)
        party_option.click()
        submit_button = self.page.get_by_role("button", name="Submit")
        submit_button.click()

    def enter_dates_and_submit(self):
        day_input = self.page.get_by_label("day")
        day_input.fill("01")
        month_input = self.page.get_by_label("month")
        month_input.fill("01")
        year_input = self.page.get_by_label("year")
        year_input.fill("2021")
        submit_button = self.page.get_by_role("button", name="Submit")
        submit_button.click()

    def test_basic_upload(self):
        self.navigate_to_home_page()
        self.upload_leaflet()
        self.fill_postcode()
        with self.mock_get_ballot_data_from_ynr([LOCAL_BALLOT_WITH_CANDIDATES]):
            self.select_time_and_submit()
            self.select_party_and_submit()
        id = self.page.url.split("/")[-2]
        expect(self.page).to_have_url(f"{self.live_server.url}/leaflets/{id}/")
        expect(self.page.locator("h1")).to_have_text("Green Party leaflet")
        heading = self.page.locator("h2", has_text="Leaflet details")
        expect(heading).to_be_visible()
        assert Leaflet.objects.get().nuts1 == "UKF"

    def test_basic_upload_ynr_down(self):
        self.navigate_to_home_page()
        self.upload_leaflet()
        self.fill_postcode()
        with self.mock_get_ballot_data_from_ynr([]):
            self.select_time_and_submit()
            self.select_party_and_submit()
        id = self.page.url.split("/")[-2]
        expect(self.page).to_have_url(f"{self.live_server.url}/leaflets/{id}/")
        expect(self.page.locator("h1")).to_have_text("Green Party leaflet")
        heading = self.page.locator("h2", has_text="Leaflet details")
        expect(heading).to_be_visible()
        assert Leaflet.objects.get().nuts1 == ""

    def test_basic_upload_more_than_one_leaflet(self):
        self.navigate_to_home_page()
        self.upload_multiple_files_for_one_leaflet()
        self.fill_postcode()
        with self.mock_get_ballot_data_from_ynr([LOCAL_BALLOT_WITH_CANDIDATES]):
            self.select_time_and_submit()
            self.select_party_and_submit()
        id = self.page.url.split("/")[-2]
        expect(self.page).to_have_url(f"{self.live_server.url}/leaflets/{id}/")
        expect(self.page.locator("h1")).to_have_text("Green Party leaflet")
        heading = self.page.locator("h2", has_text="Leaflet details")
        expect(heading).to_be_visible()
        assert LeafletImage.objects.count() == 2

    def test_upload_leaflet_with_invalid_postcode(self):
        self.upload_leaflet()
        self.fill_postcode(postcode="INVALID")
        self.select_time_and_submit()
        submit_button = self.page.get_by_role("button", name="Submit")
        submit_button.click()
        error_message = self.page.get_by_text("Please enter a full UK postcode")
        assert error_message is not None

    def test_party_page_content(self):
        self.upload_leaflet()
        self.fill_postcode()
        with self.mock_get_ballot_data_from_ynr([LOCAL_BALLOT_WITH_CANDIDATES]):
            self.select_time_and_submit()
            self.select_party_and_submit()
        id = self.page.url.split("/")[-2]
        expect(self.page).to_have_url(f"{self.live_server.url}/leaflets/{id}/")
        labour_party_link = self.page.get_by_role("link", name="Green Party")
        labour_party_link.click()
        expect(self.page.locator("h1")).to_have_text(
            "Election leaflets from Green Party"
        )

    def test_ballot_and_election_pages(self):
        leaflet = LeafletFactory()
        self.page.goto(
            urljoin(self.live_server.url, leaflet.get_absolute_url())
        )
        election_link = self.page.locator(
            "a[href='/leaflets/election/parl.2024-07-04/']"
        )
        expect(election_link).to_be_visible()
        election_link.click()
        h1 = self.page.locator("h1")
        expect(h1).to_have_text("UK Parliamentary general election")
        self.page.go_back()

        ballot_link = self.page.locator(
            "a[href='/leaflets/election/parl.newbury.2024-07-04/']"
        )
        expect(ballot_link).to_be_visible()
        ballot_link.click()
        h1 = self.page.locator("h1")
        expect(h1).to_have_text("UK Parliamentary general election: Newbury")


def test_update_publisher_details_add_person(
    db, live_server, page, admin_user, mock_get_ballot_data_from_ynr
):
    page.goto(urljoin(live_server.url, "/admin"))
    page.locator("#id_username").fill(admin_user.username)
    page.locator("#id_password").fill("password")
    page.get_by_role("button", name="Log in").click()

    with mock_get_ballot_data_from_ynr([LOCAL_BALLOT_WITH_CANDIDATES]):
        leaflet = Leaflet.objects.create(title="Test Leaflet", description=None)
        assert leaflet.ynr_party_id is None
        assert leaflet.person_ids == []
        url = urljoin(
            live_server.url,
            reverse(
                "leaflet_update_publisher_details", kwargs={"pk": leaflet.pk}
            ),
        )
        resp = page.goto(url)
    assert resp.status == 200

    page.locator("label[for=id_parties_2]").click()
    page.locator("label[for=id_people_6]").click()
    page.locator("label[for=id_people_7]").click()
    page.get_by_role("button", name="Save").click()

    leaflet.refresh_from_db()
    assert leaflet.ynr_party_id == "party:52"
    assert leaflet.person_ids == [41112, 41114]
