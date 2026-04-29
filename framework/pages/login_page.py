"""
Page Object for the Sauce Demo login page.

Encapsulates the selectors and actions for https://www.saucedemo.com
so tests stay clean and selectors live in one place.
"""
from playwright.sync_api import Page


class LoginPage:
    """Represents the Sauce Demo login page."""

    URL = "https://www.saucedemo.com/"

    # Selectors — kept in one place so they're easy to update if the UI changes
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page):
        """Store the Playwright page object."""
        self.page = page

    def open(self):
        """Navigate the browser to the login page."""
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        """Fill in the form and click Login."""
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Return the visible error message, or empty string if none."""
        if self.page.is_visible(self.ERROR_MESSAGE):
            return self.page.inner_text(self.ERROR_MESSAGE)
        return ""
