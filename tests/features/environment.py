"""Behave environment hooks for Playwright (placed under features so behave discovers it).

This mirrors the project's top-level `tests/environment.py` Playwright setup but
lives under `tests/features` so behave will automatically import it when run
from the `tests` directory.
"""
import time
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright


RESULTS_DIR = Path('results')


def before_all(context):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = RESULTS_DIR / f'run_{int(time.time())}.log'
    logging.basicConfig(filename=str(log_path), level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    context.log_file = log_path
    context.logger = logging.getLogger('behave')
    context.logger.info('Starting behave run')

    # Start Playwright and launch a headless browser for UI steps
    context._playwright = sync_playwright().start()
    browser_name = context.config.userdata.get('browser', 'chromium')
    if browser_name == 'firefox':
        context.browser = context._playwright.firefox.launch(headless=True)
    elif browser_name == 'webkit':
        context.browser = context._playwright.webkit.launch(headless=True)
    else:
        context.browser = context._playwright.chromium.launch(headless=True)

    context.page = context.browser.new_page()


def after_scenario(context, scenario):
    if scenario.status.name == 'failed':
        try:
            page = getattr(context, 'page', None)
            if page:
                screenshots = RESULTS_DIR / 'screenshots'
                screenshots.mkdir(parents=True, exist_ok=True)
                filename = screenshots / f'{scenario.name.replace(" ", "_")}_{int(time.time())}.png'
                page.screenshot(path=str(filename), full_page=True)
                context.logger.info(f'Screenshot saved to {filename}')
        except Exception as e:
            context.logger.exception('Failed to capture screenshot: %s', e)


def after_all(context):
    try:
        page = getattr(context, 'page', None)
        if page:
            page.close()
        browser = getattr(context, 'browser', None)
        if browser:
            browser.close()
        pw = getattr(context, '_playwright', None)
        if pw:
            pw.stop()
    except Exception:
        context.logger.exception('Error shutting down Playwright')

    context.logger.info('Behave run finished')
