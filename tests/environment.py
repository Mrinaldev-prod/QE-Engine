"""Behave environment hooks: Playwright setup, logging, screenshots on failure, and teardown.

This file starts a Playwright browser (sync API) before the test run and exposes
`context.page` for steps to use. On failures it captures Playwright screenshots
into `results/screenshots`.
"""
import time
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright


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

    # Start Playwright and launch a browser for UI steps
    context._playwright = sync_playwright().start()
    # Choose browser via userdata if provided; default to chromium
    browser_name = context.config.userdata.get('browser', 'chromium')
    # default to headed mode so local runs show the browser window; can be
    # overridden by passing -D headed=false to behave if needed
    headed_flag = str(context.config.userdata.get('headed', 'true')).lower()
    headed = headed_flag in ('1', 'true', 'yes')
    if browser_name == 'firefox':
        context.browser = context._playwright.firefox.launch(headless=not headed)
    elif browser_name == 'webkit':
        context.browser = context._playwright.webkit.launch(headless=not headed)
    else:
        context.browser = context._playwright.chromium.launch(headless=not headed)

    # create a browser context with video recording enabled
    results_dir = RESULTS_DIR
    videos_dir = results_dir / 'videos'
    videos_dir.mkdir(parents=True, exist_ok=True)
    context.browser_context = context.browser.new_context(record_video_dir=str(videos_dir))
    context.page = context.browser_context.new_page()


def after_scenario(context, scenario):
    # On failure, capture screenshot using Playwright page (if available)
    try:
        page = getattr(context, 'page', None)
        screenshots = RESULTS_DIR / 'screenshots'
        screenshots.mkdir(parents=True, exist_ok=True)
        vid_dir = RESULTS_DIR / 'videos'
        vid_dir.mkdir(parents=True, exist_ok=True)
        ts = int(time.time())
        safe_name = scenario.name.replace(' ', '_')
        if page:
            # always capture a screenshot for traceability
            filename = screenshots / f'{safe_name}_{ts}.png'
            try:
                page.screenshot(path=str(filename), full_page=True)
                context.logger.info(f'Screenshot saved to {filename}')
            except Exception:
                context.logger.exception('Failed to capture screenshot')

        # finalize video by closing the browser context if present; Playwright
        # writes video files on context close
        try:
            bw_ctx = getattr(context, 'browser_context', None)
            if bw_ctx:
                bw_ctx.close()
                # move the most recent webm in videos dir to a readable name
                vids = sorted(vid_dir.glob('*.webm'), key=lambda p: p.stat().st_mtime)
                if vids:
                    src = vids[-1]
                    dst = vid_dir / f'{safe_name}_{ts}.webm'
                    try:
                        src.rename(dst)
                        context.logger.info(f'Video saved to {dst}')
                    except Exception:
                        context.logger.exception('Failed to move video file')
        except Exception:
            context.logger.exception('Error finalizing video')
    except Exception:
        context.logger.exception('Error in after_scenario hooks')


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
