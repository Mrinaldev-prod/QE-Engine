from playwright.sync_api import Page, expect


class SaucedemoPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, base_url: str = "https://www.saucedemo.com/"):
        self.page.goto(base_url)

    def login(self, username: str, password: str):
        self.page.fill('input[data-test="username"]', username)
        self.page.fill('input[data-test="password"]', password)
        self.page.click('input[data-test="login-button"]')

    def is_on_inventory(self) -> bool:
        return '/inventory' in self.page.url

    def has_products_list(self) -> bool:
        try:
            expect(self.page.locator('.inventory_list')).to_be_visible(timeout=2000)
            return True
        except Exception:
            return False

    def has_login_error(self) -> bool:
        try:
            expect(self.page.locator('[data-test="error"]')).to_be_visible(timeout=2000)
            return True
        except Exception:
            return False
from playwright.sync_api import Page, TimeoutError


class SaucedemoPage:
    """Page object for saucedemo.com (login + inventory helpers)."""

    SELECTORS = {
        'username': 'input[id="user-name"]',
        'password': 'input[id="password"]',
        'login_button': 'input[id="login-button"]',
        'inventory_list': 'div.inventory_list',
        'inventory_item': '.inventory_item',
        'error_message': 'h3[data-test="error"]'
    }

    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str = 'https://www.saucedemo.com/'):
        self.page.goto(url)

    def login(self, username: str, password: str):
        self.page.fill(self.SELECTORS['username'], username)
        self.page.fill(self.SELECTORS['password'], password)
        self.page.click(self.SELECTORS['login_button'])

    def is_on_inventory(self) -> bool:
        try:
            self.page.wait_for_selector(self.SELECTORS['inventory_list'], timeout=3000)
            return '/inventory' in self.page.url or 'inventory.html' in self.page.url
        except TimeoutError:
            return False

    def has_products_list(self) -> bool:
        try:
            self.page.wait_for_selector(self.SELECTORS['inventory_item'], timeout=3000)
            return True
        except TimeoutError:
            return False

    def has_login_error(self) -> bool:
        try:
            self.page.wait_for_selector(self.SELECTORS['error_message'], timeout=3000)
            return True
        except TimeoutError:
            return False
