import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def pytest_addoption(parser):
    parser.addoption(
        '--browser', action='store', default='chrome',
        help='possibilities: chrome, firefox, edge, safari',
        choices=('chrome', 'firefox', 'edge', 'safari')
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
    elif browser == 'edge':
        driver = webdriver.Edge()
    else:
        driver = webdriver.Safari()
    yield driver
    driver.close()