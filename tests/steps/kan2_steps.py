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
    # Click only if the button exists to avoid throwing on negative tests
    locator = page.locator(selector)
    if locator.count() > 0:
        locator.click()
    else:
        # record that button was not present
        context.button_missing = True


@then('the shopping cart badge should show "{count}"')
def step_impl_cart_badge(context, count):
    page = context.page
    # The cart count element has class shopping_cart_badge on saucedemo
    badge = page.locator('.shopping_cart_badge')
    # If expecting 0, the badge is typically not present
    if int(count) == 0:
        assert badge.count() == 0, f"expected no cart badge, but found one"
        return

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


@given('the user is not logged in')
def step_user_not_logged_in(context):
    page = context.page
    # clear cookies/storage and go to the login page
    page.context.clear_cookies()
    page.goto('https://www.saucedemo.com/')


@when('the user navigates to the inventory page')
def step_navigate_inventory(context):
    page = context.page
    page.goto('https://www.saucedemo.com/inventory.html')


@then('they should be redirected to the login page')
def step_redirected_to_login(context):
    page = context.page
    # Wait for URL to be the login page
    page.wait_for_url('**/index.html', timeout=5000)
    assert '/inventory.html' not in page.url, f"Expected redirect to login, but on {page.url}"


@when('I attempt to add "{product_name}" to the cart')
def step_attempt_add(context, product_name):
    # Reuse add_to_cart implementation but record missing
    page = context.page
    btn_id = 'add-to-cart-' + product_name.lower().replace(' ', '-').replace('"', '')
    selector = f'button[id="{btn_id}"]'
    locator = page.locator(selector)
    if locator.count() > 0:
        locator.click()
        context.button_missing = False
    else:
        context.button_missing = True


@then('I should see no add-to-cart button for "{product_name}"')
def step_no_add_button(context, product_name):
    page = context.page
    btn_id = 'add-to-cart-' + product_name.lower().replace(' ', '-').replace('"', '')
    selector = f'button[id="{btn_id}"]'
    locator = page.locator(selector)
    assert locator.count() == 0, f"Expected no add button for {product_name}, but found one"


@given('the user attempts to login as "{username}" with password "{password}"')
def step_attempt_login_and_fail(context, username, password):
    page = context.page
    page.goto('https://www.saucedemo.com/')
    page.fill('#user-name', username)
    page.fill('#password', password)
    page.click('#login-button')


@then('I should see a login error message')
def step_login_error_visible(context):
    page = context.page
    err = page.locator('.error-message-container')
    err.wait_for(state='visible', timeout=5000)
    assert err.is_visible(), 'Expected login error message to be visible'
