from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchPage:
    """Page Object for storefront search interactions and results (/search)."""

    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'form[role="search"] button[type="submit"]')
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".col h6")
    EMPTY_RESULTS_MESSAGE = (By.XPATH, "//h3[contains(text(), 'No Items Match')]")

    def __init__(self, browser, live_server):
        self.browser = browser
        self.live_server = live_server
        self.wait = WebDriverWait(browser, timeout=5)

    def open(self):
        """Navigate to home page and wait for storefront search input."""
        self.browser.get(f"{self.live_server}/")
        self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        return self

    def enter_search_query(self, query):
        """Enter a query into the storefront search bar."""
        field = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        field.clear()
        field.send_keys(query)
        return self

    def click_search(self):
        """Click the search submit button."""
        btn = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        btn.click()

    def search(self, query):
        """Submit a search query and wait for navigation to /search."""
        self.enter_search_query(query)
        self.click_search()
        self.wait.until(EC.url_contains("/search"))

    def get_product_names(self):
        """Return a list of visible product names on the results page."""
        self.wait.until(EC.url_contains("/search"))
        elements = self.browser.find_elements(*self.PRODUCT_TITLES)
        return [el.text.strip() for el in elements if el.text.strip()]

    def get_empty_results_text(self):
        """Return the text of the empty-results heading when no items match."""
        elem = self.wait.until(EC.visibility_of_element_located(self.EMPTY_RESULTS_MESSAGE))
        return elem.text.strip()
