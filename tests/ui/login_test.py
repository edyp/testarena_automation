import pytest
from pages.login_page import LoginPage


def test_01(driver):
    testarena = LoginPage(driver)
    testarena.login()