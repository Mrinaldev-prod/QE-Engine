from playwright.sync_api import Page


class LoginPage:
    """Playwright-based page object for the login page.

    Expects a Playwright `Page` instance (sync API) to be passed as `page`.
    """

    SELECTORS = {
        'email': 'input[name="email"]',
        'password': 'input[name="password"]',
        'submit': 'button[type=submit]'
    }

    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def login(self, email: str, password: str):
        self.page.fill(self.SELECTORS['email'], email)
        self.page.fill(self.SELECTORS['password'], password)
        self.page.click(self.SELECTORS['submit'])
