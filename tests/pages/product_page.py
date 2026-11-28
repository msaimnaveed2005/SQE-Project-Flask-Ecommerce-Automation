from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class ProductPage:
    """Page Object for interacting with product cards rendered on storefront pages."""

    CARDS = (By.CSS_SELECTOR, "#column > .col")
    CARD_TITLE = (By.CSS_SELECTOR, "h6")
    CARD_PRICE = (By.CSS_SELECTOR, "h5")
    CARD_STOCK = (By.XPATH, ".//p[contains(text(), 'Items Left')]")
    ADD_LINK = (By.LINK_TEXT, "Add")

    def __init__(self, browser, live_server):
        self.browser = browser
        self.live_server = live_server
        self.wait = WebDriverWait(browser, timeout=5)

    def open(self, path="/"):
        """Navigate to the requested storefront path (defaults to home)."""
        self.browser.get(f"{self.live_server}{path}")
        return self

    def get_card(self, product_name):
        """Locate and return the card WebElement whose visible h6 matches product_name exactly."""
        cards = self.wait.until(EC.presence_of_all_elements_located(self.CARDS))
        for card in cards:
            try:
                title = card.find_element(*self.CARD_TITLE).text.strip()
                if title == product_name:
                    return card
            except NoSuchElementException:
                continue
        raise NoSuchElementException(f"Product card with name '{product_name}' not found.")

    def get_price(self, product_name):
        """Return the visible price text inside the selected product card."""
        card = self.get_card(product_name)
        return card.find_element(*self.CARD_PRICE).text.strip()

    def get_stock(self, product_name):
        """Return the visible stock text inside the selected product card."""
        card = self.get_card(product_name)
        return card.find_element(*self.CARD_STOCK).text.strip()

    def get_add_link(self, product_name):
        """Return the Add link WebElement inside the selected product card."""
        card = self.get_card(product_name)
        return card.find_element(*self.ADD_LINK)

    def click_add_to_cart(self, product_name):
        """Click the Add link inside the selected product card."""
        link = self.get_add_link(product_name)
        link.click()
