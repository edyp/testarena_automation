import pytest
from selenium.webdriver.common.by import By
from .main_app_page import MainAppPage


class Cockpit(MainAppPage):
    def __init__(self, driver) -> None:
        super().__init__(driver)

    def assert_all_widgets(self):
        headers = self.driver.find_elements(By.TAG_NAME, 'h4')
        exp_headers = [
            'Zadania przypisane do mnie',
            'Moje zadania',
            'Moje zadania z przekroczonym terminem',
            'Ostatnie otrzymane wiadomości'
        ]

        if len(headers) == 5:
            exp_headers.insert(0, exp_headers[0])
            self.log.debug(exp_headers)

        for i, elm in enumerate(headers):
            self.log.info(f'exp: {exp_headers[i]} in actual: {elm.text}')
            assert exp_headers[i] in elm.text
