import { expect, test } from '@playwright/test';
import fs from 'fs';
import path from 'path';

const baseUrl = 'http://localhost:8000/';

async function navigateToUploadPage(page) {
  await page.goto(baseUrl);
  await page.getByText('Upload a leaflet').click();
}

async function fillPostcode(page, postcode = 'w8 4nu') {
  await page.getByLabel('What postcode was this')
  await page.getByLabel('What postcode was this').fill(postcode); 
}

async function selectTime(page, time = 'In the last couple of weeks') {
  await page.getByText(time).click();
  await page.getByRole('button', { name: 'Submit' }).click();
}

async function selectParty(page, party = 'Labour Party') { 
  await page.getByText(party).click();
  await page.getByRole('button', { name: 'Submit' }).click();
}

// Increase the timeout for all tests
test.setTimeout(60000);

test('basic upload test', async ({ page }) => {
  await navigateToUploadPage(page);
  const testImagePath = path.resolve(__dirname, 'test_images/test_leaflet.jpeg');
  await page.getByLabel('Take a photo of a leaflet').setInputFiles(testImagePath);
  await page.getByRole('button', { name: 'Continue' }).click();
  await fillPostcode(page);
  await selectTime(page);
  await selectParty(page);
});


test('upload a leaflet from some time ago', async ({ page }) => {
  await navigateToUploadPage(page);
  const testImagePath = path.resolve(__dirname, 'test_images/test_leaflet.jpeg');
  await page.getByLabel('Take a photo of a leaflet').setInputFiles(testImagePath);
  await page.getByRole('button', { name: 'Continue' }).click();
  await fillPostcode(page);
  await selectTime(page, 'Some time ago');
  await page.locator('#id_date-date_0').fill('10');
  await page.locator('#id_date-date_0').press('Tab');
  await page.locator('#id_date-date_1').fill('10');
  await page.locator('#id_date-date_1').press('Tab');
  await page.locator('#id_date-date_2').fill('2023');
  await page.getByRole('button', { name: 'Submit' }).click();
  await selectParty(page);
});


test('uploading multiple leaflet images', async ({ page }) => {
  await navigateToUploadPage(page);
  const imageDir = path.resolve(__dirname, 'test_images/');
  const imageFiles = fs.readdirSync(imageDir).map(file => path.join(imageDir, file));
  await page.getByLabel('Take a photo of a leaflet').setInputFiles(imageFiles);
  await page.getByRole('button', { name: 'Continue' }).click();
  await fillPostcode(page);
  await selectTime(page);
  await selectParty(page);
});

test('uploading a non-image leaflet file', async ({ page }) => {
  await navigateToUploadPage(page);
  const testImagePath = path.resolve(__dirname, 'test_images/test_leaflet.docx');
  await page.getByLabel('Take a photo of a leaflet').setInputFiles(testImagePath);
  await page.getByRole('button', { name: 'Continue' }).click();
  await page.getByText('Error during upload tap to retry');
});


test('upload leaflet and visit party page', async ({ page }) => {
  await navigateToUploadPage(page);
  const testImagePath = path.resolve(__dirname, 'test_images/test_leaflet.jpeg');
  await page.getByLabel('Take a photo of a leaflet').setInputFiles(testImagePath);
  await page.getByRole('button', { name: 'Continue' }).click();
  await fillPostcode(page);
  await selectTime(page);
  await selectParty(page)   ;
  await expect (page).toHaveText('Labour Party');
  await page.getByRole('link', { name: 'Labour Party' }).click();
  await page.getByText('Election leaflets from Labour Party');
});
