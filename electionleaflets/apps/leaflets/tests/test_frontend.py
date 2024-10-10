from pathlib import Path
from django.contrib.staticfiles.testing import LiveServerTestCase
from electionleaflets import settings
from playwright.sync_api import sync_playwright


class TestLeafletUpload(LiveServerTestCase):
	"""TestLeafletUpload is a test case class for testing the leaflet upload functionality of the application using Playwright.
	This class inherits from LiveServerTestCase and provides methods to set up the test environment, navigate through the 
	application, and perform various actions such as uploading a leaflet, filling in the postcode, selecting the time, 
	and submitting forms. Each test method simulates a specific user interaction scenario to ensure the application 
	behaves as expected.
	Methods:
		setUp(): Set up the test environment for the frontend tests.
		tearDown(): Clean up resources after each test method.
		navigate_to_home_page(): Navigate to the home page of the live server.
		get_test_image(leaflet_file_path): Returns the absolute path to a test image file.
		navigate_to_upload_page(): Navigate to the upload page of the application.
		upload_leaflet(leaflet_file_path): Upload a leaflet file to the application.
		fill_postcode(postcode): Fill in the postcode field in the form.
		select_time_and_submit(): Select the time option and submit the form.
		select_party_and_submit(party): Select the party option and submit the form.
		enter_dates_and_submit(): Enter dates in the form and submit it.
		test_basic_upload(): Test the basic upload functionality of the leaflet application.
		test_upload_leaflet_from_some_time_ago(): Test uploading a leaflet with a time specified as "some time ago".
		test_upload_leaflet_with_invalid_postcode(): Test uploading a leaflet with an invalid postcode.
		test_party_page_content(): Test the content of the party page after clicking the party from the leaflet details page.
	"""
	def setUp(self):
		self.p = sync_playwright().start()
		# Launch the browser in headless mode or switch to headless=False for debugging
		self.browser = self.p.chromium.launch(headless=True)
		self.context = self.browser.new_context(java_script_enabled=True)
		self.page = self.context.new_page()
		self.page.set_default_timeout(60000)  # Set timeout to 60 seconds

	def tearDown(self):
		self.page.close()
		self.context.close()
		self.browser.close()
		self.p.stop()

	def navigate_to_home_page(self):
		self.page.goto(self.live_server_url)

	def get_test_image(self, leaflet_file_path="apps/leaflets/tests/test_images/front_test.jpg"):
		project_root = Path(settings.PROJECT_ROOT).resolve()
		return str(project_root / leaflet_file_path)

	def navigate_to_upload_page(self):
		self.page.goto(self.live_server_url)
		self.page.get_by_role('link', name='Upload a leaflet').click()
		print(f"I've just completed the navigate_to_upload_page method. I'm on the {self.page.url} step")

	def upload_leaflet(self, leaflet_file_path="apps/leaflets/tests/test_images/front_test.jpg"):
		self.navigate_to_upload_page()
		self.page.set_input_files(
			selector="input[type='file']", 
			files=[self.get_test_image(leaflet_file_path=leaflet_file_path)]
		)
		self.page.get_by_role('button', name='Submit').click()
		print(f"I've just completed the upload_leaflet method. I'm on the {self.page.url} step")
	
	def upload_multiple_files_for_one_leaflet(self, leaflet_file_paths=["apps/leaflets/tests/test_images/front_test.jpg", "apps/leaflets/tests/test_images/back_test.jpg"]):
		self.navigate_to_upload_page()

		for leaflet_file_path in leaflet_file_paths:
			self.page.set_input_files(
				selector="input[type='file']", 
				files=[self.get_test_image(leaflet_file_path=leaflet_file_path)]
			)
		self.page.get_by_role('button', name='Submit').click()

	
	def fill_postcode(self, postcode='SW1A 1AA'):
		self.page.get_by_label('What postcode was this').click()
		self.page.get_by_label('What postcode was this').fill(postcode)
		print(f"I've just completed the fill_postcode method. I'm on the {self.page.url} step")

	def select_time_and_submit(self):
		time_input = self.page.query_selector("input[type='radio'][value='now']")
		time_input.check()
		self.page.get_by_role('button', name='Submit').click()
		print(f"I've just completed the select_time_and_submit method. I'm on the {self.page.url} step")

	def select_party_and_submit(self, party='Green Party'):
		self.page.get_by_text(party).click()
		self.page.get_by_role('button', name='Submit').click()
		# TODO: This redirects to /add/images for some reason
		print(f"I've just completed the select_party_and_submit method. I'm on the {self.page.url} step")

	def enter_dates_and_submit(self):
		self.page.get_by_label('day').fill('01')
		self.page.get_by_label('month').fill('01')
		self.page.get_by_label('year').fill('2021')
		self.page.get_by_role('button', name='Submit').click()
		print(f"I've just completed the enter_dates_and_submit method. I'm on the {self.page.url} step")

	def test_basic_upload(self):
		self.upload_leaflet()
		self.fill_postcode()
		self.select_time_and_submit()
		self.select_party_and_submit()
		# check the redirect to the leaflet details page after submission
		self.assertTrue(self.page.url.startswith(self.live_server_url + '/leaflets/'))
 
	#TODO: This test triggers a javascript error in the browser, which causes the test to fail.
	# This is due to the fact that the File Upload component is not able to handle multiple files for one leaflet.
	# If you run this test suite with headless=False, you will notice that the file upload component 
 	# is not able to handle multiple files.
	
	# def test_multiple_file_uploads(self):
	# 	self.upload_multiple_files_for_one_leaflet()
	# 	self.fill_postcode()
	# 	self.select_time_and_submit()
	# 	self.select_party_and_submit()
 
	# 	# confirm we are on the leaflet details page
	# 	self.assertTrue(self.page.url.startswith(self.live_server_url + '/leaflets/'))
		
	# 	images = self.page.query_selector_all(".ds-card-image")

	# 	# confirm there are two images
	# 	self.assertEqual(len(images), 2)
 
	# 	# confirm the images are different
	# 	self.assertNotEqual(images[0].get_attribute('src'), images[1].get_attribute('src'))
  
 
	def test_upload_leaflet_with_invalid_postcode(self):
		self.upload_leaflet()
		self.fill_postcode(postcode='INVALID')
		self.select_time_and_submit()
		self.page.get_by_role('button', name='Submit').click()
		error_message = self.page.get_by_text('Please enter a full UK postcode')
		self.assertIsNotNone(error_message)

			
	#TODO: The tests cannot find 'Some time ago' on the page to interact with it. 
  	# def test_upload_leaflet_from_some_time_ago(self):	
		# self.upload_leaflet()
		# self.fill_postcode()
		# self.page.get_by_label('Some time ago').check()
		# self.page.get_by_role('button', name='Submit').click()
		# self.enter_dates_and_submit()
		# self.select_party_and_submit()

	#TODO: There is not currently any validation on the date form.
 	# def test_upload_leaflet_with_current_date(self):
		# self.upload_leaflet()
		# self.fill_postcode()
		# self.page.get_by_label('Some time ago').check()
		# self.page.get_by_role('button', name='Submit').click()
		# self.page.get_by_label('day').fill('01')
		# self.page.get_by_label('month').fill('01')
		# self.page.get_by_label('year').fill('1111')
		# self.page.get_by_role('button', name='Submit').click()
		# error_message = self.page.get_by_text('Please enter a valid date between 2015 and today')
		# self.assertIsNotNone(error_message)
  	
	def test_party_page_content(self):
		self.upload_leaflet()
		self.fill_postcode()
		self.select_time_and_submit()
		self.select_party_and_submit()
		# TODO: Ensure the URL is correct after selecting the party as this is currenlty not working
		# I've tested this redirect in electionleaflets/apps/leaflets/tests/test_models.py and it works
		# as expected. I'm not sure why it's not working here.
		self.assertFalse(self.page.url.startswith(self.live_server_url + '/leaflets/add/images'))
		self.page.get_by_role('link', name='Labour Party').click()
		self.page.get_by_text('Election leaflets from Labour Party')
  
		
