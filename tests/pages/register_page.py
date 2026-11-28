from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegisterPage:
    """Page Object for the Flask-Ecommerce signup page (/sign-up)."""

    EMAIL_INPUT = (By.ID, "email")
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD1_INPUT = (By.ID, "password1")
    PASSWORD2_INPUT = (By.ID, "password2")
    SUBMIT_BUTTON = (By.ID, "submit")
    ALERT_BOX = (By.CSS_SELECTOR, '[role="alert"]')

    def __init__(self, browser, live_server):
        self.browser = browser
        self.live_server = live_server
        self.wait = WebDriverWait(browser, timeout=5)

    def open(self):
        """Navigate to /sign-up and wait for email input to be visible."""
        self.browser.get(f"{self.live_server}/sign-up")
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        return self

    def enter_email(self, email):
        """Enter customer email."""
        field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        field.clear()
        field.send_keys(email)
        return self

    def enter_username(self, username):
        """Enter username."""
        field = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        field.clear()
        field.send_keys(username)
        return self

    def enter_password(self, password):
        """Enter password into first password field."""
        field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD1_INPUT))
        field.clear()
        field.send_keys(password)
        return self

    def enter_confirm_password(self, confirm_password):
        """Enter confirmation password into second password field."""
        field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD2_INPUT))
        field.clear()
        field.send_keys(confirm_password)
        return self

    def click_submit(self):
        """Click the submit button to register the account."""
        btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        btn.click()

    def register(self, email, username, password, confirm_password):
        """Convenience action to fill all registration fields and submit."""
        self.enter_email(email)
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(confirm_password)
        self.click_submit()

    def get_alert_text(self):
        """Wait for alert box to be visible and return its text."""
        alert = self.wait.until(EC.visibility_of_element_located(self.ALERT_BOX))
        return alert.text.strip()
