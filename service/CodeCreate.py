from playwright.sync_api import expect

from service.AssertCodes import execute_assert_code, execute_assert_using_element
from service.ActionFunctions import *
from service.WindowHandler import *
from service.WindowHandler import goto_url


def actions(pw: Playwright, page: Page, tr: TestRow, logs: Logs, element):
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
    timeout = tr.timeout
    url = tr.url
    filepath = tr.filepath

    # Variables
    code: str = ""
    receive: dict = {}
    data = None

    # Flags
    wait_flag = False
    assert_flag = False
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
    dictionary = dictionaries(page, locator, nth, value, assert_value)
    actions_dict = dictionary['actions_dict']
    assert_dict = dictionary['assert_dict']
    assert_element_dict = dictionary['assert_element_dict']

    # #1 Handle Wait ( Locator & Timeout)
    if assertion == "soft":
        try:
            if locator != "" and tr.timeout != "":
                if tr.nth != "":
                    page.locator(locator).nth(nth).wait_for(timeout=timeout)
                else:
                    page.wait_for_selector(locator, timeout=timeout)
            else:
                # print("No explicit waiting performed")
                pass
            wait_flag = True
        except Exception as e:
            wait_flag = False
    else:
        if locator != "" and tr.timeout != "" and assertion == "":
            if tr.nth != "":
                page.locator(locator).nth(nth).wait_for(timeout=timeout)
            else:
                page.wait_for_selector(locator, timeout=timeout)
        else:
            # print("No explicit waiting can be performed")
            pass
        wait_flag = True

    # #2 Handle Assertion
    if assertion != "" and element is None:
        receive = execute_assert_code(pw, page, tr, assert_dict[condition], logs)
        page = receive['page']
        assert_flag = receive['pass']
    elif assertion != "" and element is not None:
        receive = execute_assert_using_element(pw, page, tr, assert_dict[condition], logs)
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
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "inner text":
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "text content":
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "is checked":
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "is disabled":
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "is visible":
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "is hidden":
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "is enabled":
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "wait for":
                    receive = {'page': page, 'data': data}
                elif action == "wait for element state":
                    receive = {'page': page, 'data': data}
                elif action == "screenshot":
                    receive = {'page': page, 'data': data}
                elif action == "bounding box":
                    receive = {'page': page, 'data': data}
                elif action == "with text":
                    receive = {'page': page, 'data': data}
                elif action == "count":
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "all inner texts":
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "all text contents":
                    receive = execute_code_get_data(pw, page, tr, logs)
                elif action == "get page url":
                    receive = execute_code_get_data(pw, page, tr, logs)

                # Window Handler
                elif action == "open in new tab":
                    receive = open_link_in_new_tab(pw, page, tr.url, logs)
                elif action == "parent tab":
                    receive = goto_parent_tab(pw, page, logs)
                elif action == "close tab":
                    receive = close_tab(pw, page, logs)
                elif action == "loop new tab":
                    receive = open_link_in_new_tab_from_element(pw, page, element, logs)
                elif action == "open link":
                    receive = goto_url(pw, page, tr, logs)
                elif action == "page screenshot":
                    receive = page_screenshot(pw, page, tr, logs)
                elif action == "element screenshot":
                    receive = element_screenshot(pw, page, tr, logs)
                elif action == "open url":
                    receive = goto_url(pw, page, tr, logs)

                page = receive['page']
                if 'data' in receive:
                    data = receive['data']
                action_flag = True
            elif isinstance(actions_dict[action], str):
                receive = execute_code(pw, page, tr, actions_dict[action], logs)
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

    send = {'page': page, 'data': data, 'wait flag': wait_flag, 'assert flag': assert_flag, 'action flag': action_flag}
    return send


def dictionaries(page, locator, nth, value, assert_value):
    # Process Locator
    locator = locator.replace("\"", "\'")

    # Process nth
    if nth == "":
        nth = 0

    actions_dict = {
        "click": f"page.locator(\"{locator}\").nth({nth}).click()",
        "fill": f"page.locator(\"{locator}\").nth({nth}).fill(\"{value}\")",
        "press": f"page.locator(\"{locator}\").nth({nth}).press(\"{value}\")",
        "all": None,
        "store": None,
        "double click": f"page.locator(\"{locator}\").nth({nth}).double_click()",
        "focus": f"page.locator(\"{locator}\").nth({nth}).focus()",
        "hover": f"page.locator(\"{locator}\").nth({nth}).hover()",
        "select option": f"page.locator(\"{locator}\").nth({nth}).select_option(\"{value}\")",
        "select options": f"page.locator(\"{locator}\").nth({nth}).select_options({value})",
        "set input files": None,
        "text content": 1,
        "inner text": 1,
        "inner HTML": None,
        "get attribute": 1,
        "is checked": 1,
        "is disabled": 1,
        "is visible": 1,
        "is hidden": 1,
        "is enabled": 1,
        "wait for": 1,
        "wait for element state": 1,
        "screenshot": 1,
        "bounding box": 1,
        "count": 1,
        "all inner texts": 1,
        "all text contents": 1,
        "and": None,
        "filter": None,
        "first": None,
        "last": None,
        "nth": None,
        "with text": 1,
        "check": None,
        "open in new tab": 1,
        "parent tab": 1,
        "close tab": 1,
        "loop new tab": 1,
        "open link": 1,
        "page screenshot": 1,
        "element screenshot": 1,
        "open url": 1,
        "get page url": 1,
    }

    assert_dict = {
        'to be attached': f"expect(page.locator(\"{locator}\").nth({nth}),\"element not present in page/dynamic element\").to_be_attached()",
        'to be checked': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not checked\").to_be_checked()",
        'to be disabled': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not disabled\").to_be_disabled()",
        'to be editable': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not editable\").to_be_editable()",
        'to be empty': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not empty\").to_be_empty()",
        'to be enabled': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not enabled\").to_be_enabled()",
        'to be focused': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not focused\").to_be_focused()",
        'to be hidden': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not hidden\").to_be_hidden()",
        'to be in viewport': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not in viewport\").to_be_in_viewport()",
        'to be visible': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not visible\").to_be_visible()",
        'to contain text': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not contain text\").to_contain_text(\"{assert_value}\")",
        'to have accessible description': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not have accessible description\").to_have_accessible_description(\"{assert_value}\")",
        'to have accessible name': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not have accessible name\").to_have_accessible_name(\"{assert_value}\")",
        'to have attribute': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not empty\").to_have_attribute({assert_value})",
        'to have class': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not have class\").to_have_class(\"{assert_value}\")",
        'to have count': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not have count\").to_have_count(\"{assert_value}\")",
        'to have css': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not have css\").to_have_css(\"{assert_value}\")",
        'to have id': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not have id\").to_have_id(\"{assert_value}\")",
        'to have js property': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not have the js properties\").to_have_js_property({assert_value})",
        'to have role': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not have the role\").to_have_role(\"{assert_value}\")",
        'to have text': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not have the text\").to_have_text(\"{assert_value}\")",
        'to have value': f"expect(page.locator(\"{locator}\").nth({nth}),\"element does not have the value\").to_have_value(\"{assert_value}\")",
        'to have values': f"expect(page.locator(\"{locator}\").nth({nth}),\"element do not have the values \").to_have_values([{assert_value}])",
        'to have title': f"expect(\"{page}\",\"page does not have title\").to_have_title(\"{assert_value}\")",
        'to have url': f"expect(\"{page}\",\"page does not have url\").to_have_url(\"{assert_value}\")",
        'to be ok': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is not ok\").to_be_ok()",

        'not to be attached': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is present in page/dynamic element\").not_to_be_attached()",
        'not to be checked': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is checked\").not_to_be_checked()",
        'not to be disabled': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is disabled\").not_to_be_disabled()",
        'not to be editable': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is editable\").not_to_be_editable()",
        'not to be empty': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is empty\").not_to_be_empty()",
        'not to be enabled': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is enabled\").not_to_be_enabled()",
        'not to be focused': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is focused\").not_to_be_focused()",
        'not to be hidden': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is hidden\").not_to_be_hidden()",
        'not to be in viewport': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is in viewport\").not_to_be_in_viewport()",
        'not to be visible': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is visible\").not_to_be_visible()",
        'not to contain text': f"expect(page.locator(\"{locator}\").nth({nth}),\"element contains text\").not_to_contain_text(\"{assert_value}\")",
        'not to have accessible description': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has accessible description\").not_to_have_accessible_description(\"{assert_value}\")",
        'not to have accessible name': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has accessible name\").not_to_have_accessible_name(\"{assert_value}\")",
        'not to have attribute': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has attribute\").not_to_have_attribute({assert_value})",
        'not to have class': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has class\").not_to_have_class(\"{assert_value}\")",
        'not to have count': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has count\").not_to_have_count({assert_value})",
        'not to have css': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has css\").not_to_have_css(\"{assert_value}\")",
        'not to have id': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has id\").not_to_have_id(\"{assert_value}\")",
        'not to have js property': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has the js properties\").not_to_have_js_property({assert_value})",
        'not to have role': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has the role\").not_to_have_role(\"{assert_value}\")",
        'not to have text': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has the text\").not_to_have_text(\"{assert_value}\")",
        'not to have value': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has value\").not_to_have_value(\"{assert_value}\")",
        'not to have values': f"expect(page.locator(\"{locator}\").nth({nth}),\"element has values \").not_to_have_values([{assert_value}])",
        'not to have title': f"expect(\"{page}\",\"page has title\").not_to_have_title(\"{assert_value}\")",
        'not to have url': f"expect(\"{page}\",\"page has url\").not_to_have_url(\"{assert_value}\")",
        'not to be ok': f"expect(page.locator(\"{locator}\").nth({nth}),\"element is ok\").not_to_be_ok()"
    }

    assert_element_dict = {
        'to be attached': f"expect(element,\"element not present in page/dynamic element\").to_be_attached()",
        'to be checked': f"expect(element,\"element is not checked\").to_be_checked()",
        'to be disabled': f"expect(element,\"element is not disabled\").to_be_disabled()",
        'to be editable': f"expect(element,\"element is not editable\").to_be_editable()",
        'to be empty': f"expect(element,\"element is not empty\").to_be_empty()",
        'to be enabled': f"expect(element,\"element is not enabled\").to_be_enabled()",
        'to be focused': f"expect(element,\"element is not focused\").to_be_focused()",
        'to be hidden': f"expect(element,\"element is not hidden\").to_be_hidden()",
        'to be in viewport': f"expect(element,\"element is not in viewport\").to_be_in_viewport()",
        'to be visible': f"expect(element,\"element is not visible\").to_be_visible()",
        'to contain text': f"expect(element,\"element does not contain text\").to_contain_text(\"{assert_value}\")",
        'to have accessible description': f"expect(element,\"element does not have accessible description\").to_have_accessible_description(\"{assert_value}\")",
        'to have accessible name': f"expect(element,\"element does not have accessible name\").to_have_accessible_name(\"{assert_value}\")",
        'to have attribute': f"expect(element,\"element is not empty\").to_have_attribute({assert_value})",
        'to have class': f"expect(element,\"element does not have class\").to_have_class(\"{assert_value}\")",
        'to have count': f"expect(element,\"element does not have count\").to_have_count(\"{assert_value}\")",
        'to have css': f"expect(element,\"element does not have css\").to_have_css(\"{assert_value}\")",
        'to have id': f"expect(element,\"element does not have id\").to_have_id(\"{assert_value}\")",
        'to have js property': f"expect(element,\"element does not have the js properties\").to_have_js_property({assert_value})",
        'to have role': f"expect(element,\"element does not have the role\").to_have_role(\"{assert_value}\")",
        'to have text': f"expect(element,\"element does not have the text\").to_have_text(\"{assert_value}\")",
        'to have value': f"expect(element,\"element does not have the value\").to_have_value(\"{assert_value}\")",
        'to have values': f"expect(element,\"element do not have the values \").to_have_values([{assert_value}])",
        'to have title': f"expect(\"{page}\",\"page does not have title\").to_have_title(\"{assert_value}\")",
        'to have url': f"expect(\"{page}\",\"page does not have url\").to_have_url(\"{assert_value}\")",
        'to be ok': f"expect(element,\"element is not ok\").to_be_ok()",

        'not to be attached': f"expect(element,\"element is present in page/dynamic element\").not_to_be_attached()",
        'not to be checked': f"expect(element,\"element is checked\").not_to_be_checked()",
        'not to be disabled': f"expect(element,\"element is disabled\").not_to_be_disabled()",
        'not to be editable': f"expect(element,\"element is editable\").not_to_be_editable()",
        'not to be empty': f"expect(element,\"element is empty\").not_to_be_empty()",
        'not to be enabled': f"expect(element,\"element is enabled\").not_to_be_enabled()",
        'not to be focused': f"expect(element,\"element is focused\").not_to_be_focused()",
        'not to be hidden': f"expect(element,\"element is hidden\").not_to_be_hidden()",
        'not to be in viewport': f"expect(element,\"element is in viewport\").not_to_be_in_viewport()",
        'not to be visible': f"expect(element,\"element is visible\").not_to_be_visible()",
        'not to contain text': f"expect(element,\"element contains text\").not_to_contain_text(\"{assert_value}\")",
        'not to have accessible description': f"expect(element,\"element has accessible description\").not_to_have_accessible_description(\"{assert_value}\")",
        'not to have accessible name': f"expect(element,\"element has accessible name\").not_to_have_accessible_name(\"{assert_value}\")",
        'not to have attribute': f"expect(element,\"element has attribute\").not_to_have_attribute({assert_value})",
        'not to have class': f"expect(element,\"element has class\").not_to_have_class(\"{assert_value}\")",
        'not to have count': f"expect(element,\"element has count\").not_to_have_count({assert_value})",
        'not to have css': f"expect(element,\"element has css\").not_to_have_css(\"{assert_value}\")",
        'not to have id': f"expect(element,\"element has id\").not_to_have_id(\"{assert_value}\")",
        'not to have js property': f"expect(element,\"element has the js properties\").not_to_have_js_property({assert_value})",
        'not to have role': f"expect(element,\"element has the role\").not_to_have_role(\"{assert_value}\")",
        'not to have text': f"expect(element,\"element has the text\").not_to_have_text(\"{assert_value}\")",
        'not to have value': f"expect(element,\"element has value\").not_to_have_value(\"{assert_value}\")",
        'not to have values': f"expect(element,\"element has values \").not_to_have_values([{assert_value}])",
        'not to have title': f"expect(\"{page}\",\"page has title\").not_to_have_title(\"{assert_value}\")",
        'not to have url': f"expect(\"{page}\",\"page has url\").not_to_have_url(\"{assert_value}\")",
        'not to be ok': f"expect(element,\"element is ok\").not_to_be_ok()"
    }

    send = {'actions_dict': actions_dict, 'assert_dict': assert_dict, 'assert_element_dict': assert_element_dict}
    return send
