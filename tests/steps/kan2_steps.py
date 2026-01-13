from behave import given, when, then


@given('the user is logged in as "{username}" with password "{password}"')
def step_impl_login(context, username, password):
    # Use Playwright page object attached to context by environment hooks
    page = context.page
    # Open login page and sign in
    page.goto('https://www.saucedemo.com/')
    # Standard selectors for SauceDemo
    page.fill('#user-name', username)
    page.fill('#password', password)
    page.click('#login-button')
    # Ensure we're on inventory page (wait for navigation)
    page.wait_for_url('**/inventory.html')


@when('I add "{product_name}" to the cart')
def step_impl_add_to_cart(context, product_name):
    page = context.page
    # Map the product name to the expected add-to-cart button id used on saucedemo
    # e.g., Sauce Labs Backpack -> add-to-cart-sauce-labs-backpack
    btn_id = 'add-to-cart-' + product_name.lower().replace(' ', '-').replace('"', '')
    selector = f'button[id="{btn_id}"]'
    page.click(selector)


@then('the shopping cart badge should show "{count}"')
def step_impl_cart_badge(context, count):
    page = context.page
    # The cart count element has class shopping_cart_badge on saucedemo
    badge = page.locator('.shopping_cart_badge')
    badge.wait_for(state='visible', timeout=5000)
    assert badge.inner_text().strip() == str(count), f"expected cart badge {count}, got {badge.inner_text()}"


@then('the product "{product_name}" should show a Remove button')
def step_impl_product_remove_button(context, product_name):
    page = context.page
    # Remove button id pattern: remove-sauce-labs-backpack
    btn_id = 'remove-' + product_name.lower().replace(' ', '-').replace('"', '')
    selector = f'button[id="{btn_id}"]'
    btn = page.locator(selector)
    btn.wait_for(state='visible', timeout=5000)
    assert btn.is_visible(), f"Remove button for {product_name} not visible"
