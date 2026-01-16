from playwright.sync_api import Page, TimeoutError


class InventoryPage:
    """Playwright helpers for the Swab Labs inventory page."""

    SELECTORS = {
        'inventory_item': '.inventory_item',
        'item_name': '.inventory_item_name',
        'add_to_cart_btn': 'button[id^="add-to-cart-"]',
        'shopping_cart_badge': '.shopping_cart_badge',
        'cart_link': 'a.shopping_cart_link'
    }

    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str = 'https://www.saucedemo.com/inventory.html'):
        self.page.goto(url)

    def add_item_to_cart(self, item_text: str) -> bool:
        # find the inventory item by name and click its add button
        items = self.page.query_selector_all(self.SELECTORS['inventory_item'])
        for item in items:
            name_el = item.query_selector(self.SELECTORS['item_name'])
            if name_el and name_el.inner_text().strip() == item_text:
                btn = item.query_selector('button')
                if btn:
                    btn.click()
                    return True
        return False

    def cart_count(self) -> int:
        badge = self.page.query_selector(self.SELECTORS['shopping_cart_badge'])
        if badge:
            try:
                return int(badge.inner_text().strip())
            except Exception:
                return 0
        return 0

    def cart_contains(self, item_text: str) -> bool:
        # navigate to cart and check items
        self.page.click(self.SELECTORS['cart_link'])
        try:
            self.page.wait_for_selector('.cart_item', timeout=3000)
            items = self.page.query_selector_all('.cart_item .inventory_item_name')
            for it in items:
                if it.inner_text().strip() == item_text:
                    return True
            return False
        except TimeoutError:
            return False
