from behave import given, when, then
from pages.saucedemo_page import SaucedemoPage


@given('the browser is on the login page')
def step_open_login(context):
    base_url = context.config.userdata.get('base_url', 'https://www.saucedemo.com/')
    context.sauce = SaucedemoPage(context.page)
    context.sauce.open(base_url)


@when('I enter username "{username}" and password "{password}"')
def step_enter_credentials(context, username, password):
    context.sauce.login(username, password)


@when('I submit the login form')
def step_submit_form(context):
    # login method already clicks submit; nothing extra needed here
    pass


@then('I should be taken to the inventory page')
def step_check_inventory(context):
    assert context.sauce.is_on_inventory(), f"Not on inventory page: {context.page.url}"


@then('I should see the products list')
def step_see_products(context):
    assert context.sauce.has_products_list(), "Products list not visible"


@then('I should remain on the login page')
def step_remain_on_login(context):
    assert not context.sauce.is_on_inventory(), f"Unexpectedly on inventory: {context.page.url}"


@then('I should see a login error message')
def step_see_login_error(context):
    assert context.sauce.has_login_error(), "Expected login error message not found"
