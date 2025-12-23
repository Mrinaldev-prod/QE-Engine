from behave import given, when, then
from appium import webdriver as appium_driver


@given('the mobile app is launched')
def launch_app(context):
    # Example capabilities - override via userdata or env vars
    caps = {
        'platformName': context.config.userdata.get('platformName', 'Android'),
        'deviceName': context.config.userdata.get('deviceName', 'emulator-5554'),
        'app': context.config.userdata.get('app_path', '/path/to/app.apk')
    }
    context.driver = appium_driver.Remote(context.config.userdata.get('appium_server', 'http://localhost:4723/wd/hub'), caps)


@when('the user logs in with valid credentials')
def mobile_login(context):
    # Implement mobile-specific selectors
    d = context.driver
    d.find_element('accessibility id', 'email').send_keys('test@example.com')
    d.find_element('accessibility id', 'password').send_keys('Password123!')
    d.find_element('accessibility id', 'login').click()


@then('the user sees the dashboard screen')
def check_dashboard(context):
    # Simple heuristic - replace with proper assertion
    assert context.driver.find_elements('accessibility id', 'dashboard')
