from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from common.logger import Logger
from .credentials_page import TestarenaCredentialsPage
from .cockpit_page import Cockpit


class LoginPage:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.url = 'http://demo.testarena.pl/zaloguj'
        self.unsuccessful_login_url = 'http://demo.testarena.pl/logowanie'
        self.log = Logger()

        self.email_field = (By.ID, 'email')
        self.password_field = (By.ID, 'password')
        self.captcha = (By.CLASS_NAME, 'g-recaptcha ')
        self.captcha_checkbox = (By.CLASS_NAME, 'rc-anchor-checkbox-holder')
        self.captcha_img_select = (By.ID, 'id="rc-imageselect"')
        self.login_button = (By.ID, 'save')
        self.error_notifications = (By.CLASS_NAME, 'login_form_error')
        self.error_captcha = (By.CLASS_NAME, 'error_msg')


    def login(self):
        credentials = TestarenaCredentialsPage(self.driver)
        self.driver.get(self.url)
        if self.active_captcha():
            self.log.critical('###### Active reCAPTCHA - STOPPING TESTS ######')
            pytest.skip("According to active reCAPTCHA test need to be skipped.")
        self.fill_form(credentials.username, credentials.password)
        cockpit_page = Cockpit(self.driver)
        assert self.driver.current_url == cockpit_page.url
        assert self.driver.get_cookie('FrameProfile') is not None
        self.log.info('################ LOG IN SUCESSFUL ################')
        cockpit_page.assert_all_widgets()
        return cockpit_page

    def fill_form(self, email, password, submit=True):
        self.log.info(f'username: {email}; password: {password}')
        email_field = self.driver.find_element(*(self.email_field))
        password_field = self.driver.find_element(*(self.password_field))
        login_button = self.driver.find_element(*(self.login_button))
        email_field.send_keys(str(email))
        password_field.send_keys(str(password))
        if submit:
            login_button.click()

    def clear_fields(self):
        self.driver.find_element(*(self.email_field)).clear()
        self.driver.find_element(*(self.password_field)).clear()

    def email_field_text(self):
        email_field = self.driver.find_element(*(self.email_field))
        return email_field.get_attribute('value')

    def error_notifications_list(self):
        error_elms = self.driver.find_elements(*(self.error_notifications))
        notyfications = [x.get_attribute('innerText') for x in error_elms]
        self.log.info('Errors:' + '\n'.join(notyfications))
        return notyfications

    def captcha_error_text(self):
        captcha_error = self.driver.find_element(*(self.error_captcha))
        return captcha_error.get_attribute('innerText')

    def active_captcha(self):
        try:
            self.driver.find_element(*(self.captcha))
        except NoSuchElementException:
            return False
        return True
