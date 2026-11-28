from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object for the Flask-Ecommerce login page (/login)."""

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "submit")
    ALERT_BOX = (By.CSS_SELECTOR, '[role="alert"]')

    def __init__(self, browser, live_server):
        self.browser = browser
        self.live_server = live_server
        self.wait = WebDriverWait(browser, timeout=5)

    def open(self):
        """Navigate to /login and wait for email input to be visible."""
        self.browser.get(f"{self.live_server}/login")
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        return self

    def enter_email(self, email):
        """Enter customer email into the email field."""
        field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        field.clear()
        field.send_keys(email)
        return self

    def enter_password(self, password):
        """Enter password into the password field."""
        field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        field.clear()
        field.send_keys(password)
        return self

    def click_submit(self):
        """Click the submit button to submit credentials."""
        btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        btn.click()

    def login(self, email, password):
        """Convenience action to fill email and password and submit."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()

    def get_alert_text(self):
        """Wait for alert box to be visible and return its text."""
        alert = self.wait.until(EC.visibility_of_element_located(self.ALERT_BOX))
        return alert.text.strip()
