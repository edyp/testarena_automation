from time import sleep
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from common.logger import Logger


class CoreAppPage:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.log = Logger()
        self.url = None
        # sidebar
        self.tasks = (By.XPATH, '//a[contains(@href, \'tasks\')]')
        # here should be listed all locators from sidebar
        # header 
        self.project_dropdown = (By.ID, 'activeProject_chosen')
        self.project_search = (By.XPATH, '//div[contains(@class, "chosen-search")/input]')
        self.logout_button = (By.CLASS_NAME, 'header_logout')
        # here should be listed all locators from header
        # modal
        self.success_modal = (By.ID, 'j_info_box')
        self.close_modal = (By.CLASS_NAME, 'j_close_button')
        # here should be other locators which can be inheritted by other pages

    def select_project(self, name):
        if name != self.get_active_project():
            self.driver.find_element(self.project_dropdown).click()
            search = self.driver.find_element(self.project_search)
            search.send_keys(name)
            search.send_keys(Keys.Enter)
            assert self.driver.find_element(self.project_dropdown).text == name

    def logout(self):
        self.driver.find_element(*(self.logout_button)).click()
        assert self.driver.current_url == 'http://demo.testarena.pl/zaloguj'
        assert self.driver.get_cookie('FrameProfile') is None
        self.log.info('################ LOG OUT SUCESSFUL ################')

    def get_active_project(self):
        return self.driver.find_element(self.project_dropdown).text

    def load_page(self):
        self.driver.get(self.url)
    
    def type_text(self, locator, text):
        field = self.driver.find_element(*locator)
        field.send_keys(text)

    def type_tag(self, locator, text):
        field = self.driver.find_element(*locator)
        field.send_keys(text)
        sleep(0.5)
        field.send_keys(Keys.ARROW_DOWN)
        field.send_keys(Keys.ENTER)

    def select(self, locator, value):
        select = Select(self.driver.find_element(*locator))
        select.select_by_value(value)

    def assert_confirmation_modal(self, text, close=True):
        modal = self.driver.find_element(*(self.success_modal))
        assert modal.is_displayed()
        assert text == modal.get_attribute('innerText')

        if close:
            self.driver.find_element(*(self.close_modal)).click()
