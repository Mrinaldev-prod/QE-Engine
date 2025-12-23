# QE-Engine — Testing framework scaffold

This repository includes a scaffolding for UI, API and Mobile testing using:

- Python
- Behave (Cucumber-style BDD)
- Appium (for mobile)
- Selenium (for web UI)
- Allure for reporting

Quick start

1. Create a python virtualenv and install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run unit tests:

```bash
./scripts/run_tests.sh unit
```

3. Run smoke BDD tests (UI + API):

```bash
./scripts/run_tests.sh smoke
```

4. Run mobile E2E tests (requires Appium server and device/emulator):

```bash
./scripts/run_tests.sh e2e
```

5. Generate and view Allure report (install Allure CLI locally):

```bash
# after running tests
allure serve results/allure-results
```

Local git hook

Place the script `scripts/git-hooks/pre-push` in `.git/hooks/pre-push` (or run `scripts/install_hooks.sh`) to run unit tests automatically before push.

CI

The GitHub Actions workflow `.github/workflows/qa-ci.yml` will run unit, smoke, e2e and regression suites on PRs. The workflow uploads Allure results as artifacts.

Extending the scaffold

- Add page objects to `tests/pages/` for UI.
- Add API clients to `tests/api_client.py`.
- Add real Appium capabilities in Behave userdata or environment variables.
