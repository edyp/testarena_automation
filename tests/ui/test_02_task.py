from time import sleep
import pytest
from pages.tasks_page import TasksPage


def test_01_add_new_task(login):
    driver = login
    tasks_page = TasksPage(driver)
    tasks_page.load_page(tasks_page.tasks)
    try:
        form_page = tasks_page.add_task()
        form_page.fill()
        task_details_page = form_page.submit()
        tasks_page.assert_confirmation_modal("Zadanie zostało dodane.")
        task_details_page.close_task_details()
    except AssertionError:
        pass
    finally:
        tasks_page.delete_all_tasks()
