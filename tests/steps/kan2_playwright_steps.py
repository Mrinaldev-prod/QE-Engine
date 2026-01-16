from behave import given, when, then
from tests.pages.inventory_page import InventoryPage


@given('the browser is on the inventory page')
def given_on_inventory(context):
    base = context.config.userdata.get('inventory_url', 'https://www.saucedemo.com/inventory.html')
    context.inventory = InventoryPage(context.page)
    context.inventory.open(base)


@when('I add the "{item}" to cart')
def when_add_item(context, item):
    added = context.inventory.add_item_to_cart(item)
    assert added, f"Failed to find and add item: {item}"


@then('the cart count should be "{count}"')
def then_cart_count(context, count):
    expected = int(count)
    actual = context.inventory.cart_count()
    assert actual == expected, f"Expected cart count {expected} but got {actual}"


@then('the cart should contain "{item}"')
def then_cart_contains(context, item):
    assert context.inventory.cart_contains(item), f"Cart does not contain expected item: {item}"
