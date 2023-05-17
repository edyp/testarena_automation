import json
import pytest
from selenium.common.exceptions import NoSuchElementException
from pages.login_page import LoginPage
from pages.core_app_page import CoreAppPage
from common.logger import Logger

LOG = Logger()
def get_credentials(group):
    path='common/static/credentials.json'
    with open(path) as task_data_f:
        credentials = json.load(task_data_f)
        LOG.info('Incorrect credentials provided.')
        return credentials[group]

@pytest.fixture
def logout_after(driver):
    yield
    if driver.get_cookie('FrameProfile') is not None:
        CoreAppPage(driver).logout()

@pytest.fixture
def clear_fields(driver):
    yield
    LoginPage(driver).clear_fields()

def failed_login_test_template(driver, credentials, error_msg_list):
    login_page = LoginPage(driver)
    login_page.fill_form(credentials['username'], credentials['password'])
    assert login_page.unsuccessful_login_url == driver.current_url
    assert login_page.email_field_text() == credentials['username'][:320]
    assert login_page.error_notifications_list() == error_msg_list
    if login_page.active_captcha():
        assert login_page.captcha_error_text() == 'Nie uzupełniono pola captcha.'

@pytest.mark.parametrize('credentials', get_credentials('incorrect_format_email'))
def test_ioncorrect_format_email_login(driver, logout, credentials, clear_fields):
    error_msg_list = ['Nieprawidłowy format adresu e-mail. Wprowadź adres ponownie.',
                      'Adres e-mail i/lub hasło są niepoprawne.']
    failed_login_test_template(driver, credentials, error_msg_list)

@pytest.mark.parametrize('credentials', get_credentials('incorrect_email'))
def test_incorrect_email_login(driver, credentials, clear_fields):
    error_msg_list = ['Nieprawidłowy adres e-mail. Wprowadź adres ponownie.',
                      'Adres e-mail i/lub hasło są niepoprawne.']
    failed_login_test_template(driver, credentials, error_msg_list)

@pytest.mark.parametrize('credentials', get_credentials('not_registered_email'))
def test_not_registered_email_login(driver, credentials, clear_fields):
    error_msg_list = ['Adres e-mail i/lub hasło są niepoprawne.']
    failed_login_test_template(driver, credentials, error_msg_list)

@pytest.mark.parametrize('credentials', get_credentials('empty_email'))
def test_empty_email(driver, credentials, clear_fields):
    error_msg_list = ['Pole wymagane', 'Adres e-mail i/lub hasło są niepoprawne.']
    failed_login_test_template(driver, credentials, error_msg_list)

@pytest.mark.parametrize('credentials', get_credentials('empty_password'))
def test_empty_password(driver, credentials, clear_fields):
    error_msg_list = ['Pole wymagane', 'Adres e-mail i/lub hasło są niepoprawne.']
    failed_login_test_template(driver, credentials, error_msg_list)

@pytest.mark.parametrize('credentials', get_credentials('empty_form'))
def test_empty_form(driver, credentials, clear_fields):
    error_msg_list = ['Pole wymagane', 'Pole wymagane']
    failed_login_test_template(driver, credentials, error_msg_list)
