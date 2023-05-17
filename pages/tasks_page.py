from time import sleep
import pytest
from selenium.webdriver.common.by import By
from .core_app_page import CoreAppPage


class TasksPage(CoreAppPage):
    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.url = 'http://demo.testarena.pl/KK/tasks'
        self.add_task_button = (By.CLASS_NAME, 'button_link_nav')
        self.select_all_button = (By.ID, 'j_multiSelect_selectAllButton_task3306')
        self.delete_selected = (By.CLASS_NAME, 'j_delete_tasks')
        self.empty_task_list = (By.CLASS_NAME, 'empty-text')
        self.confirm_dialog_buttons = (By.CLASS_NAME, 'ui-button-text-only')

    def add_task(self):
        self.driver.find_element(*(self.add_task_button)).click()
        assert self.driver.current_url == 'http://demo.testarena.pl/KK/task_add'
        assert "Dodaj zadanie" in self.driver.title
        return AddTaskForm(self.driver)

    def delete_all_tasks(self):
        self.driver.find_element(*(self.select_all_button)).click()
        sleep(0.5)
        self.driver.find_element(*(self.delete_selected)).click()
        self.driver.find_elements(*(self.confirm_dialog_buttons))[0].click()
        self.assert_confirmation_modal("Zadania zostały usunięte.")
        assert self.driver.find_element(*(self.empty_task_list)).is_displayed()


class AddTaskForm(CoreAppPage):
    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.url = 'http://demo.testarena.pl/KK/task_add'
        self.title = (By.ID, 'title')
        self.description = (By.ID, 'description')
        self.release = (By.ID, 'releaseName')
        self.environments = (By.ID, 'token-input-environments')
        self.versions = (By.ID, 'token-input-versions')
        self.priority = (By.ID, 'priority')
        self.due_date = (By.ID, 'dueDate')
        self.assignee = (By.ID, 'assigneeName')
        self.tags = (By.ID, 'token-input-tags')
        self.save_button = (By.ID, 'save')
        self.cancel_button = (By.CLASS_NAME, 'j_cancel_button')

    def fill(self, data):
        self.type_text(self.title, data['title'])
        self.type_text(self.description, data['description'])
        self.type_tag(self.release, data['release'])
        self.type_tag(self.environments, data['environment'])
        self.type_tag(self.versions, data['version'])
        self.select(self.priority, data['priority'])
        self.type_text(self.due_date, data['due_date'])
        self.type_tag(self.assignee, data['assignee'])
        self.type_tag(self.tags, data['tag'])

    def submit(self):
        self.driver.find_element(*(self.save_button)).click()
        assert 'task_view' in self.driver.current_url
        return TaskDetailsPage(self.driver)
    
    def cancel(self):
        self.driver.find_element(*(self.cancel_button)).click()
        assert TasksPage().url == self.driver.current_url


class TaskDetailsPage(CoreAppPage):
    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.url = 'http://demo.testarena.pl/KK/task_view/'
        self.back_button = (By.XPATH, '//nav[@class="button_link_nav"]/ul/li')

    def close_task_details(self):
        self.driver.find_element(*(self.back_button)).click()