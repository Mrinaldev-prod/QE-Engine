"""Behave environment hooks: set up logging, screenshots on failure, and teardown."""
import os
import time
import logging
from pathlib import Path


RESULTS_DIR = Path('results')


def before_all(context):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    # simple logging setup
    log_path = RESULTS_DIR / f'run_{int(time.time())}.log'
    logging.basicConfig(filename=str(log_path), level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    context.log_file = log_path
    context.logger = logging.getLogger('behave')
    context.logger.info('Starting behave run')


def after_scenario(context, scenario):
    # On failure, try to capture screenshot if a driver exists
    if scenario.status.name == 'failed':
        try:
            driver = getattr(context, 'driver', None)
            if driver:
                screenshots = RESULTS_DIR / 'screenshots'
                screenshots.mkdir(parents=True, exist_ok=True)
                filename = screenshots / f'{scenario.name.replace(" ", "_")}_{int(time.time())}.png'
                # different drivers have different screenshot APIs
                if hasattr(driver, 'get_screenshot_as_file'):
                    driver.get_screenshot_as_file(str(filename))
                elif hasattr(driver, 'save_screenshot'):
                    driver.save_screenshot(str(filename))
                context.logger.info(f'Screenshot saved to {filename}')
        except Exception as e:
            context.logger.exception('Failed to capture screenshot: %s', e)


def after_all(context):
    context.logger.info('Behave run finished')
