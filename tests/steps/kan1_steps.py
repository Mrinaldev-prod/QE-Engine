from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

# Lightweight driver factory — replace with project fixtures if available
def _get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)

@given('the browser is on the login page')
def step_given_browser_on_login(context):
    url = os.environ.get('LOGIN_URL', 'https://www.saucedemo.com/')
    context.driver = _get_driver()
    context.driver.get(url)

@when('I enter username "{username}" and password "{password}"')
def step_when_enter_credentials(context, username, password):
    u = context.driver.find_element(By.ID, 'user-name')
    p = context.driver.find_element(By.ID, 'password')
    u.clear(); u.send_keys(username)
    p.clear(); p.send_keys(password)

@when('I submit the login form')
def step_when_submit(context):
    btn = context.driver.find_element(By.ID, 'login-button')
    btn.click()
    time.sleep(1)

@then('I should be taken to the inventory page')
def step_then_inventory(context):
    context.driver.implicitly_wait(3)
    assert 'inventory' in context.driver.current_url

@then('I should see the products list')
def step_then_products(context):
    items = context.driver.find_elements(By.CLASS_NAME, 'inventory_item')
    assert len(items) > 0

@then('I should remain on the login page')
def step_then_remain_login(context):
    context.driver.implicitly_wait(1)
    assert 'saucedemo.com' in context.driver.current_url

@then('I should see a login error message')
def step_then_error(context):
    err = context.driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
    assert err is not None and err.text.strip() != ''

# Teardown

def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        context.driver.quit()
