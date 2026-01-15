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
    assert 'home' in context.page.url
