import json
from time import sleep
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .main_app_page import MainAppPage


class TasksPage(MainAppPage):
    def __init__(self, driver) -> None:
        super().__init__(driver)

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


class AddTaskForm(MainAppPage):
    def __init__(self, driver) -> None:
        super().__init__(driver)

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

    def _load_task_data(self, path='common/static/task_data.json'):
        with open(path) as task_data_f:
            return json.load(task_data_f)

    def fill(self, data=None):
        if data is None:
            data = self._load_task_data()
        task = data['correct']
        self.type_text(self.title, task['title'])
        self.type_text(self.description, task['description'])
        self.type_tag(self.release, task['release'])
        self.type_tag(self.environments, task['environment'])
        self.type_tag(self.versions, task['version'])
        self.select(self.priority, task['priority'])
        self.type_text(self.due_date, task['due_date'])
        self.type_tag(self.assignee, task['assignee'])
        self.type_tag(self.tags, task['tag'])

    def submit(self):
        self.driver.find_element(*(self.save_button)).click()
        assert 'task_view' in self.driver.current_url
        return TaskDetailsPage(self.driver)


class TaskDetailsPage(MainAppPage):
    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.back_button = (By.XPATH, '//nav[@class="button_link_nav"]/ul/li')

    def close_task_details(self):
        self.driver.find_element(*(self.back_button)).click()