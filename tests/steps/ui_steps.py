from behave import given, when, then
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


@given('the user opens the login page')
def open_login(context):
    # Simple Chrome driver instantiation; replace options as needed
    context.driver = webdriver.Chrome(ChromeDriverManager().install())
    context.driver.get(context.config.userdata.get('base_url', 'https://example.com/login'))


@when('the user submits valid credentials')
def submit_credentials(context):
    # Placeholder selectors; adapt to your app
    driver = context.driver
    driver.find_element('name', 'email').send_keys('test@example.com')
    driver.find_element('name', 'password').send_keys('Password123!')
    driver.find_element('css selector', 'button[type=submit]').click()


@then('the user should be redirected to the home page')
def check_home(context):
    assert 'home' in context.driver.current_url
