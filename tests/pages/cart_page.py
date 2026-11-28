from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class CartPage:
    """Page Object for interacting with the shopping cart page (/cart)."""

    ROW_ITEMS = (By.CSS_SELECTOR, ".card-body > .row")
    TOTAL_AMOUNT = (By.ID, "totalamount")
    SUBTOTAL_AMOUNT = (By.ID, "amount_tt")
    EMPTY_CART_MESSAGE = (By.XPATH, "//h1[contains(text(), 'Your Cart is Empty')]")

    def __init__(self, browser, live_server):
        self.browser = browser
        self.live_server = live_server
        self.wait = WebDriverWait(browser, timeout=5)

    def open(self):
        """Navigate to /cart and wait for page to render."""
        self.browser.get(f"{self.live_server}/cart")
        return self

    def get_row(self, product_name):
        """Locate candidate rows with .card-body > .row and select the one matching product_name."""
        rows = self.wait.until(EC.presence_of_all_elements_located(self.ROW_ITEMS))
        for row in rows:
            try:
                title = row.find_element(By.TAG_NAME, "h3").text.strip()
                if title == product_name:
                    return row
            except NoSuchElementException:
                continue
        raise NoSuchElementException(f"Cart row for product '{product_name}' not found.")

    def get_quantity(self, product_name):
        """Return the visible quantity string from the product's scoped row."""
        row = self.get_row(product_name)
        qty_elem = row.find_element(By.XPATH, ".//span[@id='quantity']")
        return qty_elem.text.strip()

    def click_plus(self, product_name):
        """Click the plus (+) control inside the product's scoped row."""
        row = self.get_row(product_name)
        plus_btn = row.find_element(By.CSS_SELECTOR, ".plus-cart")
        plus_btn.click()

    def click_minus(self, product_name):
        """Click the minus (-) control inside the product's scoped row."""
        row = self.get_row(product_name)
        minus_btn = row.find_element(By.CSS_SELECTOR, ".minus-cart")
        minus_btn.click()

    def click_remove(self, product_name):
        """Click the Remove control inside the product's scoped row."""
        row = self.get_row(product_name)
        remove_btn = row.find_element(By.CSS_SELECTOR, ".remove-cart")
        remove_btn.click()

    def get_total(self):
        """Return the visible total amount string from the cart summary."""
        total_elem = self.wait.until(EC.visibility_of_element_located(self.TOTAL_AMOUNT))
        return total_elem.text.strip()

    def get_subtotal(self):
        """Return the visible subtotal amount string from the cart summary."""
        subtotal_elem = self.wait.until(EC.visibility_of_element_located(self.SUBTOTAL_AMOUNT))
        return subtotal_elem.text.strip()

    def get_empty_cart_text(self):
        """Return the visible empty cart heading text."""
        elem = self.wait.until(EC.visibility_of_element_located(self.EMPTY_CART_MESSAGE))
        return elem.text.strip()
