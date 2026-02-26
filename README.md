# QA Engineer Assignment Test - MIFX

Test script for API [reqres.in](https://reqres.in/api/users?page=2) and Web [saucedemo.com](https://www.saucedemo.com/). Cover positive and negative case with some assumptions.

# Tech Stack

1. Python
   - python-dotenv: read env file.
   - httpx: http client.
   - allure-pytest: plugin test documentation.
   - pytest-playwright: plugin provides a robust and flexible way to write end-to-end (E2E) tests for web applications using the Pytest framework and the Playwright library.
   - pytest-xdist: run test on parallel mode.
2. NodeJS
   - allure report: open test report with format HTML.

# Prerequisites

1. Install [Python](https://www.python.org/)
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
3. Install [NodeJS](https://nodejs.org/en/download)
4. Install [Allure Report](https://allurereport.org/docs/v3/install/)

# How to run

1. Create virtual env `uv venv`.
2. Activate virtual env `source .venv/bin/activate` for Linux/macOS or `.venv\Scripts\activate` for Windows.
3. Run command `uv sync` to install all deps.
4. Install browser `playwright install`.
5. Run test `uv run pytest -s -vv -n auto --alluredir test-report .`.
6. Open test report `allure serve --port 8080 test-report/`.
