import traceback as tb_cls
import pytest
from pages.tasks_page import (TasksPage, TaskDetailsPage)


def test_add_new_task(login, task_testing_data, driver):
    tasks_page = TasksPage(driver)
    tasks_page.load_page()
    form_page = tasks_page.add_task()
    form_page.fill(task_testing_data['correct'])
    try:
        task_details_page = form_page.submit()
        tasks_page.assert_confirmation_modal("Zadanie zostało dodane.")
        task_details_page.close_task_details()
    except AssertionError as ae:
        tasks_page.log.error(ae)
        tb_strings = tb_cls.format_list(tb_cls.extract_tb(ae.__traceback__))
        tasks_page.log.error('AssertionError traceback:\n' + ''.join(tb_strings))
    finally:
        if tasks_page.url == driver.current_url:
            tasks_page.delete_all_tasks()
        elif form_page.url == driver.current_url:
            form_page.cancel()
        else:
            TaskDetailsPage(driver).close_task_details()
            tasks_page.delete_all_tasks()
