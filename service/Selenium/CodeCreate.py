from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

from entity.ExcelData import TestRow
from service.Selenium.ActionFunctions import *
from service.Selenium.AssertCodes import *
from service.Selenium.WindowHandler import *


def actions(driver, tr: TestRow, logs, element=None):
    logs.log.info(f"Working with Actions in with row details: {vars(tr)}")

    # Cell Values
    description = tr.description
    execute = tr.execute
    locator = tr.locator
    nth = tr.nth
    action = tr.action
    value = tr.value
    assertion = tr.assertion
    condition = tr.condition
    assert_value = tr.assert_value
    key = tr.stored_value_key
    timeout = tr.timeout or 3  # Default timeout to 3 seconds
    url = tr.url
    filepath = tr.filepath

    # Variables
    code: str = ""
    receive: dict = {}
    data = None

    # Flags
    wait_flag = False
    assert_flag = True
    action_flag = False

    # Process Locator
    locator = locator.replace("\"", "\'")

    # Process Timeout
    if tr.timeout == "":
        timeout = 3000

    # Process nth
    if tr.nth == "":
        nth = 0

    # Process assertion
    assertion = assertion.lower()

    # Dictionaries
    dictionary = dictionaries(driver, locator, nth, value, assert_value)
    actions_dict = dictionary['actions_dict']
    assert_dict = dictionary['assert_dict']
    assert_element_dict = dictionary['assert_element_dict']

    # #1 Handle Wait (Locator & Timeout)
    if assertion.lower() == "soft":
        try:
            if locator:
                if nth:
                    wait = WebDriverWait(driver, timeout)
                    wait.until(EC.presence_of_element_located((By.XPATH, f"({locator})[{nth}]")))
                else:
                    wait = WebDriverWait(driver, timeout)
                    wait.until(EC.presence_of_element_located((By.XPATH, locator)))
            wait_flag = True
        except Exception:
            wait_flag = False
    else:
        if locator and assertion == "":
            if nth:
                wait = WebDriverWait(driver, timeout)
                wait.until(EC.presence_of_element_located((By.XPATH, f"({locator})[{nth}]")))
            else:
                wait = WebDriverWait(driver, timeout)
                wait.until(EC.presence_of_element_located((By.XPATH, locator)))
            wait_flag = True

    # #2 Handle Assertion
    if assertion != "" and element is None:
        receive = execute_assert_code(driver, tr, assert_dict[condition], logs)
        driver = receive['page']
        assert_flag = receive['pass']
    elif assertion != "" and element is not None:
        receive = execute_assert_using_element(driver, tr, assert_element_dict[condition], logs)
        page = receive['page']
        assert_flag = receive['pass']
    else:
        # print("No assertions to be performed")
        assert_flag = True

    # #3 Perform Action
    if assert_flag:
        if action != "":
            if actions_dict[action] == 1:
                # Returns Data
                if action == "get attribute":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "inner text":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "text content":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "is checked":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "is disabled":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "is visible":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "is hidden":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "is enabled":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "wait for":
                    receive = {'page': driver, 'data': data}
                elif action == "wait for element state":
                    receive = {'page': driver, 'data': data}
                elif action == "screenshot":
                    receive = {'page': driver, 'data': data}
                elif action == "bounding box":
                    receive = {'page': driver, 'data': data}
                elif action == "with text":
                    receive = {'page': driver, 'data': data}
                elif action == "count":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "all inner texts":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "all text contents":
                    receive = execute_code_get_data(driver, tr, logs)
                elif action == "get page url":
                    receive = execute_code_get_data(driver, tr, logs)

                # Window Handler
                elif action == "open in new tab":
                    receive = open_link_in_new_tab(driver, tr.url, logs)
                elif action == "parent tab":
                    receive = goto_parent_tab(driver, logs)
                elif action == "close tab":
                    receive = close_tab(driver, logs)
                elif action == "loop new tab":
                    receive = open_link_in_new_tab_from_element(driver, element, logs)
                elif action == "open link":
                    receive = goto_url(driver, tr, logs)
                elif action == "page screenshot":
                    receive = page_screenshot(driver, tr, logs)
                elif action == "element screenshot":
                    receive = element_screenshot(driver, tr, logs)
                elif action == "open url":
                    receive = goto_url(driver, tr, logs)

                page = receive['page']
                if 'data' in receive:
                    data = receive['data']
                action_flag = True
            elif isinstance(actions_dict[action], str):
                receive = execute_code(driver, tr, actions_dict[action], logs)
                page = receive['page']
                action_flag = True

            else:
                # print("Action not defined")
                action_flag = False
        else:
            # print("No action to be performed")
            action_flag = True
    else:
        action_flag = False
    send = {'page': driver, 'data': data, 'wait flag': wait_flag, 'assert flag': assert_flag,
            'action flag': action_flag}
    return send


from selenium.webdriver.common.by import By


def dictionaries(driver, locator, nth, value, assert_value):
    # Process Locator
    locator = locator.replace("\"", "\'")

    # Process nth
    if nth == "":
        nth = 0

    actions_dict = {
        "click": f"driver.find_elements(By.XPATH, \"{locator}\")[{nth}].click()",
        "fill": f"driver.find_elements(By.XPATH, \"{locator}\")[{nth}].send_keys(\"{value}\")",
        "press": f"driver.find_elements(By.XPATH, \"{locator}\")[{nth}].send_keys(Keys.{value})",
        "double click": f"webdriver.ActionChains(driver).double_click(driver.find_elements(By.XPATH, \"{locator}\")[{nth}]).perform()",
        "focus": f"driver.find_elements(By.XPATH, \"{locator}\")[{nth}].click()",
        "hover": f"webdriver.ActionChains(driver).move_to_element(driver.find_elements(By.XPATH, \"{locator}\")[{nth}]).perform()",
        "select option": f"select(driver.find_elements(By.XPATH, \"{locator}\")[{nth}]).select_by_visible_text(\"{value}\")",
        "select options": f"select(driver.find_elements(By.XPATH, \"{locator}\")[{nth}]).select_by_value(\"{value}\")",
        "text content": 1,
        "inner text": 1,
        "get attribute": 1,
        "is checked": 1,
        "is disabled": 1,
        "is visible": 1,
        "is hidden": 1,
        "is enabled": 1,
        "screenshot": 1,
        "count": 1,
        "all inner texts": 1,
        "all text contents": 1,
        "open in new tab": 1,
        "close tab": 1,
        "open url": 1,
    }

    assert_dict = {
        'to be checked': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_selected(), 'Element is not checked'",
        'to be disabled': f"assert not driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_enabled(), 'Element is not disabled'",
        'to be visible': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_displayed(), 'Element is not visible'",
        'to be editable': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_enabled(), 'Element is not editable'",
        'to be empty': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].text == '', 'Element is not empty'",
        'to be enabled': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_enabled(), 'Element is not enabled'",
        'to be focused': f"assert driver.switch_to.active_element == driver.find_elements(By.XPATH, \"{locator}\")[{nth}], 'Element is not focused'",
        'to be hidden': f"assert not driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_displayed(), 'Element is not hidden'",
        'to be in viewport': f"assert driver.execute_script('return arguments[0].getBoundingClientRect().top >= 0 && arguments[0].getBoundingClientRect().bottom <= window.innerHeight', driver.find_elements(By.XPATH, \"{locator}\")[{nth}]), 'Element is not in viewport'",
        'to contain text': f"assert '{assert_value}' in driver.find_elements(By.XPATH, \"{locator}\")[{nth}].text, 'Element does not contain the expected text'",
        'to have text': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].text == \"{assert_value}\", 'Element does not have the expected text'",
        'to have attribute': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].get_attribute('{assert_value}') is not None, 'Element does not have the attribute'",
        'to have value': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].get_attribute('value') == \"{assert_value}\", 'Element does not have the expected value'",
        'to have title': f"assert driver.title == \"{assert_value}\", 'Page does not have the expected title'",
        'to have url': f"assert driver.current_url == \"{assert_value}\", 'Page does not have the expected URL'",
        'to be ok': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_enabled() and driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_displayed(), 'Element is not ok'",

        # Negated assertions
        'not to be checked': f"assert not driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_selected(), 'Element is checked'",
        'not to be disabled': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_enabled(), 'Element is disabled'",
        'not to be visible': f"assert not driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_displayed(), 'Element is visible'",
        'not to be editable': f"assert not driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_enabled(), 'Element is editable'",
        'not to be empty': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].text != '', 'Element is empty'",
        'not to be enabled': f"assert not driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_enabled(), 'Element is enabled'",
        'not to be focused': f"assert driver.switch_to.active_element != driver.find_elements(By.XPATH, \"{locator}\")[{nth}], 'Element is focused'",
        'not to be hidden': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_displayed(), 'Element is hidden'",
        'not to be in viewport': f"assert not driver.execute_script('return arguments[0].getBoundingClientRect().top >= 0 && arguments[0].getBoundingClientRect().bottom <= window.innerHeight', driver.find_elements(By.XPATH, \"{locator}\")[{nth}]), 'Element is in viewport'",
        'not to contain text': f"assert '{assert_value}' not in driver.find_elements(By.XPATH, \"{locator}\")[{nth}].text, 'Element contains text'",
        'not to have text': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].text != \"{assert_value}\", 'Element has the text'",
        'not to have attribute': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].get_attribute('{assert_value}') is None, 'Element has attribute'",
        'not to have value': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].get_attribute('value') != \"{assert_value}\", 'Element has value'",
        'not to have title': f"assert driver.title != \"{assert_value}\", 'Page has title'",
        'not to have url': f"assert driver.current_url != \"{assert_value}\", 'Page has url'",
        'not to be ok': f"assert driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_enabled() and driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_displayed(), 'Element is ok'",
    }

    assert_element_dict = {
        'to be attached': f"assert element is not None, 'Element not present in page/dynamic element'",
        'to be checked': f"assert element.is_selected(), 'Element is not checked'",
        'to be disabled': f"assert not element.is_enabled(), 'Element is not disabled'",
        'to be editable': f"assert element.is_enabled(), 'Element is not editable'",
        'to be empty': f"assert element.text == '', 'Element is not empty'",
        'to be enabled': f"assert element.is_enabled(), 'Element is not enabled'",
        'to be focused': f"assert driver.switch_to.active_element == element, 'Element is not focused'",
        'to be hidden': f"assert not element.is_displayed(), 'Element is not hidden'",
        'to be in viewport': f"assert driver.execute_script('return arguments[0].getBoundingClientRect().top >= 0 && arguments[0].getBoundingClientRect().bottom <= window.innerHeight', element), 'Element is not in viewport'",
        'to be visible': f"assert element.is_displayed(), 'Element is not visible'",
        'to contain text': f"assert '{assert_value}' in element.text, 'Element does not contain text'",
        'to have accessible description': f"assert element.get_attribute('aria-describedby') == \"{assert_value}\", 'Element does not have accessible description'",
        'to have accessible name': f"assert element.get_attribute('aria-label') == \"{assert_value}\", 'Element does not have accessible name'",
        'to have attribute': f"assert element.get_attribute('{assert_value}') is not None, 'Element does not have the attribute'",
        'to have class': f"assert '{assert_value}' in element.get_attribute('class'), 'Element does not have the class'",
        'to have count': f"assert len(driver.find_elements(By.XPATH, \"{locator}\")) == {assert_value}, 'Element does not have the expected count'",
        'to have css': f"assert element.value_of_css_property('{assert_value}') is not None, 'Element does not have css'",
        'to have id': f"assert element.get_attribute('id') == \"{assert_value}\", 'Element does not have the id'",
        'to have js property': f"assert driver.execute_script('return arguments[0].{assert_value}', element) is not None, 'Element does not have the js property'",
        'to have role': f"assert element.get_attribute('role') == \"{assert_value}\", 'Element does not have the role'",
        'to have text': f"assert element.text == \"{assert_value}\", 'Element does not have the expected text'",
        'to have value': f"assert element.get_attribute('value') == \"{assert_value}\", 'Element does not have the expected value'",
        'to have values': f"assert element.get_attribute('value') in [{assert_value}], 'Element does not have the expected values'",
        'to have title': f"assert driver.title == \"{assert_value}\", 'Page does not have the expected title'",
        'to have url': f"assert driver.current_url == \"{assert_value}\", 'Page does not have the expected URL'",
        'to be ok': f"assert element.is_enabled() and element.is_displayed(), 'Element is not ok'",

        # Negated assertions
        'not to be attached': f"assert element is None, 'Element is present in page/dynamic element'",
        'not to be checked': f"assert not element.is_selected(), 'Element is checked'",
        'not to be disabled': f"assert element.is_enabled(), 'Element is disabled'",
        'not to be editable': f"assert not element.is_enabled(), 'Element is editable'",
        'not to be empty': f"assert element.text != '', 'Element is empty'",
        'not to be enabled': f"assert not element.is_enabled(), 'Element is enabled'",
        'not to be focused': f"assert driver.switch_to.active_element != element, 'Element is focused'",
        'not to be hidden': f"assert element.is_displayed(), 'Element is hidden'",
        'not to be in viewport': f"assert not driver.execute_script('return arguments[0].getBoundingClientRect().top >= 0 && arguments[0].getBoundingClientRect().bottom <= window.innerHeight', element), 'Element is in viewport'",
        'not to be visible': f"assert not element.is_displayed(), 'Element is visible'",
        'not to contain text': f"assert '{assert_value}' not in element.text, 'Element contains text'",
        'not to have accessible description': f"assert element.get_attribute('aria-describedby') != \"{assert_value}\", 'Element has accessible description'",
        'not to have accessible name': f"assert element.get_attribute('aria-label') != \"{assert_value}\", 'Element has accessible name'",
        'not to have attribute': f"assert element.get_attribute('{assert_value}') is None, 'Element has attribute'",
        'not to have class': f"assert '{assert_value}' not in element.get_attribute('class'), 'Element has class'",
        'not to have count': f"assert len(driver.find_elements(By.XPATH, \"{locator}\")) != {assert_value}, 'Element has count'",
        'not to have css': f"assert element.value_of_css_property('{assert_value}') is None, 'Element has css'",
        'not to have id': f"assert element.get_attribute('id') != \"{assert_value}\", 'Element has id'",
        'not to have js property': f"assert driver.execute_script('return arguments[0].{assert_value}', element) is None, 'Element has the js property'",
        'not to have role': f"assert element.get_attribute('role') != \"{assert_value}\", 'Element has the role'",
        'not to have text': f"assert element.text != \"{assert_value}\", 'Element has the text'",
        'not to have value': f"assert element.get_attribute('value') != \"{assert_value}\", 'Element has value'",
        'not to have values': f"assert element.get_attribute('value') not in [{assert_value}], 'Element has values'",
        'not to have title': f"assert driver.title != \"{assert_value}\", 'Page has title'",
        'not to have url': f"assert driver.current_url != \"{assert_value}\", 'Page has url'",
        'not to be ok': f"assert not (element.is_enabled() and element.is_displayed()), 'Element is ok'"
    }

    send = {'actions_dict': actions_dict, 'assert_dict': assert_dict, 'assert_element_dict': assert_element_dict}
    return send
