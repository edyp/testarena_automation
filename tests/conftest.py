import json
import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.core_app_page import CoreAppPage


def pytest_addoption(parser):
    parser.addoption(
        '--browser', action='store', default='chrome',
        help='Choose browser you have on your machine.',
        choices=('chrome', 'firefox', 'safari')
    )

@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption('--browser')

@pytest.fixture(scope='session')
def driver(browser):
    if browser == 'chrome':
        driver = webdriver.Chrome()
    elif browser == 'firefox':
        driver = webdriver.Firefox()
        driver.implicitly_wait(5)
    else:
        driver = webdriver.Safari()
    yield driver
    driver.close()

@pytest.fixture
def login(driver):
    if driver.get_cookie('FrameProfile') is None:
        testarena = LoginPage(driver)
        cockpit_page = testarena.login()
        cockpit_page.assert_all_widgets()

@pytest.fixture
def logout(driver):
    if driver.get_cookie('FrameProfile') is not None:
        CoreAppPage(driver).logout()

@pytest.fixture
def task_testing_data():
    path='common/static/task_data.json'
    with open(path) as task_data_f:
        return json.load(task_data_f)