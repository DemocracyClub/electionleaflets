import pytest
from pathlib import Path
from electionleaflets import settings
from playwright.sync_api import Page, expect


class TestLeafletUpload():
	@pytest.fixture(autouse=True)
	def setup_method(self, page: Page, live_server):
		self.page = page
		self.live_server = live_server

	def navigate_to_home_page(self):
		
		self.page.goto(self.live_server.url)

	def get_test_image(self, leaflet_file_path="apps/leaflets/tests/test_images/front_test.jpg"):
		project_root = Path(settings.PROJECT_ROOT).resolve()
		return [str(project_root / leaflet_file_path)]

	def navigate_to_upload_page(self):
		upload_link = self.page.get_by_role('link', name='Upload a leaflet')
		upload_link.click(timeout=60000)
		expect(self.page).to_have_url(f'{self.live_server.url}/leaflets/add/images/')
		take_photo_link = self.page.get_by_label('Take a photo of a leaflet')
		take_photo_link.click(timeout=60000)

	def upload_leaflet(self):
		self.navigate_to_home_page()
		self.navigate_to_upload_page()
		files = self.get_test_image()
		self.page.set_input_files(selector='input[type="file"]', files=files)
		submit_button = self.page.get_by_role('button', name='Continue')
		submit_button.click()

	def upload_multiple_files_for_one_leaflet(self):
		self.navigate_to_home_page()
		self.navigate_to_upload_page()
		files = self.get_test_image()
		self.page.set_input_files(selector='input[type="file"]', files=files)    
		add_another_image = self.page.get_by_text('Add another image')
		add_another_image.click()
		self.page.set_input_files(selector='input[type="file"]', files=files)
		submit_button = self.page.get_by_role('button', name='Continue')
		submit_button.click()

	def fill_postcode(self, postcode='SW1A 1AA'):
		postcode_input = self.page.get_by_label('What postcode was this')
		postcode_input.click()
		postcode_input.fill(postcode)

	def select_time_and_submit(self):
		time_input = self.page.get_by_text('In the last couple of weeks')
		time_input.check()
		submit_button = self.page.get_by_role('button', name='Submit')
		submit_button.click()

	def select_party_and_submit(self, party='Green Party'):
		party_option = self.page.get_by_text(party)
		party_option.click()
		submit_button = self.page.get_by_role('button', name='Submit')
		submit_button.click()

	def enter_dates_and_submit(self):
		day_input = self.page.get_by_label('day')
		day_input.fill('01')
		month_input = self.page.get_by_label('month')
		month_input.fill('01')
		year_input = self.page.get_by_label('year')
		year_input.fill('2021')
		submit_button = self.page.get_by_role('button', name='Submit')
		submit_button.click()

	def test_basic_upload(self):
		self.navigate_to_home_page()
		self.upload_leaflet()
		self.fill_postcode()
		self.select_time_and_submit()
		self.select_party_and_submit()
		id = self.page.url.split('/')[-2]
		expect(self.page).to_have_url(f'{self.live_server.url}/leaflets/{id}/')
		expect(self.page.locator('h1')).to_have_text(f'Leaflet #{id}')
		expect(self.page.locator('h2')).to_have_text('Leaflet details')

	def test_upload_leaflet_with_invalid_postcode(self):
		self.upload_leaflet()
		self.fill_postcode(postcode='INVALID')
		self.select_time_and_submit()
		submit_button = self.page.get_by_role('button', name='Submit')
		submit_button.click()
		error_message = self.page.get_by_text('Please enter a full UK postcode')
		assert error_message is not None

	def test_party_page_content(self):
		self.upload_leaflet()
		self.fill_postcode()
		self.select_time_and_submit()
		self.select_party_and_submit()
		id = self.page.url.split('/')[-2]
		expect(self.page).to_have_url(f'{self.live_server.url}/leaflets/{id}/')
		labour_party_link = self.page.get_by_role('link', name='Green Party')
		labour_party_link.click()
		expect(self.page.locator('h1')).to_have_text('Election leaflets from Green Party')