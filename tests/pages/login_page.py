from selenium.webdriver.common.by import By


class LoginPage:
    EMAIL = (By.NAME, 'email')
    PASSWORD = (By.NAME, 'password')
    SUBMIT = (By.CSS_SELECTOR, 'button[type=submit]')

    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def login(self, email, password):
        self.driver.find_element(*self.EMAIL).send_keys(email)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.SUBMIT).click()
