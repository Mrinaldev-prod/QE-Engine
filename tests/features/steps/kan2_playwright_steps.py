from behave import given, when, then
from pages.inventory_page import InventoryPage
from pages.saucedemo_page import SaucedemoPage


@given('the browser is on the inventory page')
def step_open_inventory(context):
    base_url = context.config.userdata.get('base_url', 'https://www.saucedemo.com/inventory.html')
    context.inventory = InventoryPage(context.page)
    context.sauce = SaucedemoPage(context.page)
    context.inventory.open(base_url)
    # If redirected to login, perform a quick login with standard_user
    if context.page.query_selector('input[data-test="username"]'):
        context.sauce.login('standard_user', 'secret_sauce')
    # wait for inventory to load
    context.page.wait_for_selector(context.inventory.SELECTORS['inventory_item'], timeout=7000)


@when('I add the "{item}" to cart')
def step_add_item(context, item):
    # ensure items are present before attempting to add
    context.page.wait_for_selector(context.inventory.SELECTORS['inventory_item'], timeout=5000)
    added = context.inventory.add_item_to_cart(item)
    assert added, f"Failed to add item to cart: {item}"


@then('the cart count should be "{count}"')
def step_cart_count(context, count):
    # wait briefly for badge to update
    actual = context.inventory.cart_count()
    assert str(actual) == str(count), f"Expected cart count {count}, got {actual}"


@then('the cart should contain "{item}"')
def step_cart_contains(context, item):
    contains = context.inventory.cart_contains(item)
    assert contains, f"Cart does not contain expected item: {item}"
