import pytest
from selenium.webdriver.common.by import By
from common.logger import Logger
from .credentials_page import TestarenaCredentialsPage
from .cockpit_page import Cockpit

class LoginPage:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.url = 'http://demo.testarena.pl/zaloguj'
        self.log = Logger()
        self.credentials = TestarenaCredentialsPage(self.driver)

    def login(self):
        self.driver.get(self.url)
        email = self.driver.find_element(By.ID, 'email')
        password = self.driver.find_element(By.ID, 'password')
        login_button = self.driver.find_element(By.ID, 'save')
        email.send_keys(self.credentials.username)
        password.send_keys(self.credentials.password)
        login_button.click()
        assert self.driver.current_url == 'http://demo.testarena.pl/'
        assert self.driver.get_cookie('FrameProfile') is not None
        cockpit_page = Cockpit(self.driver)
        cockpit_page.assert_all_widgets()
        return cockpit_page
