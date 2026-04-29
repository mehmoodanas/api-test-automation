"""
End-to-end browser tests for the Sauce Demo login flow.

Uses LoginPage and InventoryPage Page Objects from framework/pages/.
"""
import pytest

from framework.pages.login_page import LoginPage
from framework.pages.inventory_page import InventoryPage


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login_lands_on_inventory(page):
    """A standard user lands on the inventory page after login."""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    assert "inventory" in page.url
    assert inventory.is_loaded()
    assert inventory.title_text() == "Products"
    assert login_page.get_error_message() == ""


@pytest.mark.ui
@pytest.mark.smoke
def test_inventory_shows_six_products(page):
    """After login the inventory page shows exactly 6 products."""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    assert inventory.item_count() == 6


@pytest.mark.ui
@pytest.mark.negative
def test_locked_out_user_sees_error(page):
    """A locked-out user sees a clear error message and stays on the login page."""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("locked_out_user", "secret_sauce")

    error = login_page.get_error_message()
    assert "locked out" in error.lower()
    assert "inventory" not in page.url


@pytest.mark.ui
@pytest.mark.negative
def test_login_with_wrong_password_shows_error(page):
    """A wrong password produces a 'Username and password do not match' error."""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "definitely_wrong")

    error = login_page.get_error_message()
    assert error != ""
    assert "inventory" not in page.url
