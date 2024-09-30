Playwright tests exist in /tests. Before running any of the following commands, make sure you have installed the dependencies by running `npm install` and started the server by running `pipenv python manage.py runserver`. 

  npx playwright test
    Runs the end-to-end tests.

  npx playwright test --ui
    Starts the interactive UI mode.

  npx playwright test --project=chromium
    Runs the tests only on Desktop Chrome.

  npx playwright test example
    Runs the tests in a specific file.

  npx playwright test --debug
    Runs the tests in debug mode.

  npx playwright codegen
    Auto generate tests with Codegen.

We suggest that you begin by typing:

    npx playwright test

Visit https://playwright.dev/docs/intro for more information. ✨