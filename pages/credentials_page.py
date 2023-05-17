import pytest
from selenium.webdriver.common.by import By
from common.logger import Logger


class TestarenaCredentialsPage:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.url = 'http://testarena.pl/demo'
        self.log = Logger()
        self._get_credentials()

    def _get_credentials(self):
        self.driver.get(self.url)
        elm = self.driver.find_element(By.XPATH, '//div[@class="description"]')
        copy = [x for x in elm.text.splitlines() if 'Login' in x or 'Hasło' in x]
        self.log.debug(copy)
        self.username = copy[0].split(': ')[1]
        self.password = copy[1].split(': ')[1]
        self.log.info(f'{self.username}:{self.password}')
        self.log.debug(f'{type(self.username)}:{type(self.password)}')

        assert self.username is not None
        assert self.password is not None