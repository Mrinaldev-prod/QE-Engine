from playwright.sync_api import Page


class LoginPage:
    """Playwright-based page object for the login page.

    Expects a Playwright `Page` instance (sync API) to be passed as `page`.
    """

    SELECTORS = {
        # Primary (generic) selectors; fallback logic in `login` will try
        # multiple common variants so tests are resilient across targets.
        'email': 'input[name="email"]',
        'password': 'input[name="password"]',
        'submit': 'button[type=submit]'
    }

    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def login(self, email: str, password: str):
        # Attempt a few common email/username selectors for robustness.
        email_selectors = [
            self.SELECTORS.get('email'),
            'input#user-name',
            'input[name="user-name"]',
            'input[name="username"]',
            'input[type="email"]',
        ]
        password_selectors = [
            self.SELECTORS.get('password'),
            'input#password',
            'input[name="password"]',
            'input[type="password"]',
        ]
        submit_selectors = [
            self.SELECTORS.get('submit'),
            'button#login-button',
            'button[type=submit]',
        ]

        for sel in email_selectors:
            if not sel:
                continue
            try:
                if self.page.query_selector(sel):
                    self.page.fill(sel, email)
                    break
            except Exception:
                continue

        for sel in password_selectors:
            if not sel:
                continue
            try:
                if self.page.query_selector(sel):
                    self.page.fill(sel, password)
                    break
            except Exception:
                continue

        for sel in submit_selectors:
            if not sel:
                continue
            try:
                if self.page.query_selector(sel):
                    self.page.click(sel)
                    return
            except Exception:
                continue
        # As a last resort, try pressing Enter in the password field
        try:
            self.page.keyboard.press('Enter')
        except Exception:
            pass
