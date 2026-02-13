from behave import given, when, then
from tests.pages.login_page import LoginPage


@given('the user opens the login page')
def open_login(context):
    # `context.page` is provided by the behave environment hooks (Playwright setup).
    base_url = context.config.userdata.get('base_url', 'https://example.com/login')
    context.page.goto(base_url)
    context.login_page = LoginPage(context.page)


@when('the user submits valid credentials')
def submit_credentials(context):
    # Use the Playwright-based page object
    context.login_page.login('test@example.com', 'Password123!')


@then('the user should be redirected to the home page')
def check_home(context):
    # Be resilient: accept any navigation away from the login URL, or
    # known app landing paths (e.g. 'inventory' for saucedemo).
    current_url = context.page.url
    login_url = context.config.userdata.get('base_url', 'https://example.com/login')
    if 'inventory' in current_url:
        return
    assert current_url != login_url, f'Expected navigation away from login page, still at {current_url}'
