# QE-Engine

A compact, developer-friendly engine for Quality Engineering (QE) workflows — automation scaffolding, test harness patterns, and developer tooling to accelerate reliable, repeatable QA and verification work.

This repository provides an opinionated starting point for building test automation frameworks, experiment pipelines, and small CI-friendly test runners. It focuses on clarity, easy extensibility, and pragmatic conventions so teams can get productive quickly.

## Quick overview

- Purpose: provide a lightweight, maintainable base for creating automated tests and verification pipelines.
- Audience: QA engineers, test automation developers, and engineers who want a reproducible test harness.
- Scope: scaffolding, developer workflows, example patterns — not a full-featured test platform out of the box.

## Key features

- Clear project structure and recommended conventions.
- Minimal dependencies and easy adaptation to existing test frameworks (pytest, jest, mocha, etc.).
- Templates for test runners, reporting, and CI integration.
- Guidance for local development, debugging, and contributing.

## Prerequisites

- macOS / Linux / Windows (developer workstation)
- Git
- A language runtime / test framework of your choice (this repo is framework-agnostic; see project structure)

Note: add language-specific prerequisites (Node.js, Python, Java, etc.) in this README or a dedicated CONTRIBUTING.md when the repository adds implementation files.

## Getting started (example)

1. Clone the repository:

```bash
git clone https://github.com/Mrinaldev-prod/QE-Engine.git
cd QE-Engine
```

2. Inspect the project structure and pick a language/test runner you want to adopt.

3. Create your test harness following the conventions described below.

## Quickstart — Python + Playwright (example)

This project includes a small Python/Behave + Playwright testing scaffold. The steps below will get you running the smoke examples locally and show how CI generates Allure reports and publishes an HTML report to GitHub Pages.

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers (required for UI tests):

```bash
python3 -m playwright install
```

4. Run the test runner script (creates timestamped run logs and Allure results):

```bash
./scripts/run_tests.sh
# The script will create `results/run_<timestamp>.log` and `results/allure-results` when tests run.
```

5. (Optional) Generate an Allure HTML report locally:

```bash
# If you have the Allure CLI installed locally (e.g. via Homebrew on macOS):
allure generate results/allure-results -o results/allure-report --clean
ls -la results/allure-report
```

Notes:
- The smoke tests included in `tests/features` point to example placeholders by default (e.g. `example.com`). Provide real `base_url`/`api_base` values via behave userdata when running in your environment, or edit the feature files for local demo pages.
- The `scripts/run_tests.sh` script will attempt to call the Allure CLI after test execution if it is present on the PATH.

## Recommended project structure

This repository intentionally starts minimal. When you add code, consider the following layout:

- /docs — design notes, architecture decisions, and runbooks
- /src or /lib — implementation code for the test harness or engine
- /tests — automated tests and examples
- /ci — CI configs, small helpers and scripts
- README.md — this file
- CONTRIBUTING.md — contribution and development guidelines

Example (language-specific)

- For Python projects:
	- `pyproject.toml` or `requirements.txt`
	- `src/` with package code
	- `tests/` with pytest tests


## Development notes

- Keep the core engine minimal and implement language-specific adapters as separate modules.
- Prefer simple, well-documented scripts for common tasks like running tests, generating reports, or packaging artifacts.
- Aim for a fast local developer loop: short-running unit tests, deterministic fixtures, and reproducible data.

## CI and reporting

- This repository uses GitHub Actions to run test jobs and to collect Allure results.
- The CI workflow additionally downloads/pins an Allure CLI release, generates an HTML report from `results/allure-results`, and publishes the generated HTML to GitHub Pages (the CI workflow includes a `publish_report` job that deploys the site). After the workflow runs, the report will be available under the repository's Pages URL (for example: `https://Mrinaldev-prod.github.io/QE-Engine/`) once Pages is configured and the workflow completes successfully.

If you want reports published to an S3 bucket instead, we can add an optional job that uploads the generated HTML to S3 (this requires providing AWS credentials via repository secrets).

## Contributing

Contributions are welcome. A minimal contribution flow:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Add tests for new behavior.
4. Open a pull request describing the change.

Add a `CONTRIBUTING.md` if you want project-specific guidelines (commit style, PR template, code owner rules, etc.).

## License

This project is provided under the terms of the LICENSE file in this repository.

---

If you'd like, I can:

- add a language-specific example (Python or Node) with a tiny test harness and CI config,
- create a `CONTRIBUTING.md` and PR checklist,
- or add quickstart scripts for running local tests.

Recent automation tasks:

- Generated KAN-2 test artifacts (feature, Playwright page object, step definitions) based on Jira issue `KAN-2`.
- If you'd like these committed and submitted as a PR, run the helper script or allow the automation to push a `feat/kan2-tests` branch and open a PR.

<!-- PR automation note: PR created by automation will appear under feat/kan2-tests -->

Tell me which of the above you'd like and I'll scaffold it next.