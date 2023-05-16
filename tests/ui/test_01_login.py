import pytest
from pages.login_page import LoginPage


def test_01_correct_login(driver):
    testarena = LoginPage(driver)
    testarena.login()
