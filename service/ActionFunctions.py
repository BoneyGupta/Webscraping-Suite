import time

from playwright.sync_api import Playwright, Page, expect

from entity.ExcelData import TestRow
from service.Logger import Logs


def execute_code_get_data(pw: Playwright, page: Page, tr: TestRow, logs: Logs):
    logs.log.info(f"(ActionFunctions/execute_code_get_data) {vars(tr)}")

    # Variables
    data = ""

    # Process Locator
    locator = tr.locator.replace("\"", "\'")

    # Process Timeout
    timeout = tr.timeout
    if tr.timeout == "":
        timeout = 3000

    # Process nth
    nth = tr.nth
    if tr.nth == "":
        nth = 0

    # Process assertion
    assertion = tr.assertion.lower()

    if tr.action == "get attribute":
        logs.code_prog.info(f"data = page.locator(\"{locator}\").nth({nth}).get_attribute(\"{tr.value}\")")
        data = page.locator(locator).nth(nth).get_attribute(f"{tr.value}")
    elif tr.action == "is checked":
        logs.code_prog.info(f"data = page.locator(\"{locator}\").nth({nth}).is_checked()")
        data = page.locator(locator).nth(nth).is_checked()
    elif tr.action == "is disabled":
        logs.code_prog.info(f"data = page.locator(\"{locator}\").nth({nth}).is_disabled()")
        data = page.locator(locator).nth(nth).is_disabled()
    elif tr.action == "is visible":
        logs.code_prog.info(f"data = page.locator(\"{locator}\").nth({nth}).is_visible")
        data = page.locator(locator).nth(nth).is_visible()
    elif tr.action == "is hidden":
        logs.code_prog.info(f"data = page.locator(\"{locator}\").nth({nth}).is_hidden()")
        data = page.locator(locator).nth(nth).is_hidden()
    elif tr.action == "is enabled":
        logs.code_prog.info(f"data = page.locator(\"{locator}\").nth({nth}).is_enabled()")
        data = page.locator(locator).nth(nth).is_enabled()
    elif tr.action == "wait for":
        pass
    elif tr.action == "wait for element state":
        pass
    elif tr.action == "screenshot":
        pass
    elif tr.action == "bounding box":
        pass
    elif tr.action == "with text":
        pass
    elif tr.action == "count":
        logs.code_prog.info(f"data = page.locator(\"{locator}\").nth({nth}).count()")
        data = page.locator(locator).nth(nth).count()
    elif tr.action == "inner text":
        logs.code_prog.info(f"data = page.locator(\"{locator}\").nth({nth}).inner_text()")
        data = page.locator(locator).nth(nth).inner_text()
    elif tr.action == "text content":
        logs.code_prog.info(f"data = page.locator({locator}).nth({nth}).text_content()")
        data = page.locator(locator).nth(nth).text_content()
    elif tr.action == "all inner texts":
        logs.code_prog.info(
            f"data = page.locator({locator}).nth({nth}).all_inner_texts()")
        data = page.locator(locator).nth(nth).all_inner_texts()
    elif tr.action == "all text contents":
        logs.code_prog.info(
            f"data = page.locator(\"{locator}\").nth({nth})all_text_contents()")
        data = page.locator(locator).nth(nth).all_text_contents()
    elif tr.action == "get page url":
        logs.code_prog.info(f"data = page.url")
        data = page.url
    elif tr.execute != "":
        exec_str = f"data = {tr.execute}"
        logs.code_prog.info(exec_str)
        if assertion == 'soft':
            try:
                exec(exec_str)
            except Exception as e:
                logs.log.info(f"Execute Failed: {exec_str} Error: {str(e)}")
                print(f"Error: {str(e)}")
        else:
            exec(exec_str)
    else:
        data = ""

    send = {'page': page, 'data': data}
    return send


def execute_code(pw: Playwright, page: Page, tr: TestRow, exec_str: str, logs: Logs):
    logs.log.info(f"(ActionFunctions/execute_code) {exec_str}")

    # Process assertion
    assertion = tr.assertion.lower()

    logs.code_prog.info(exec_str)
    if assertion == 'soft':
        try:
            exec(exec_str)
        except Exception as e:
            logs.log.info(f"Execute Failed: {exec_str} Error: {str(e)}")
            print(f"Error: {str(e)}")
    else:
        exec(exec_str)

    send = {'page': page}
    return send


def page_screenshot(pw: Playwright, page: Page, tr: TestRow, logs: Logs):
    logs.log.info(f"(ActionFunctions/page_screenshot) {vars(tr)}")

    logs.code_prog.info(
        f"page.wait_for_load_state(\"load\")\npage.screenshot(path=f\"{logs.directory_path}\\pgscrnsht{time.strftime('%H%M%S')}{tr.filepath}\", timeout=100000)")
    page.wait_for_load_state("load")
    page.screenshot(path=f"{logs.directory_path}\\pgscrnsht{time.strftime('%H%M%S')}{tr.filepath}", timeout=100000)
    send = {'page': page}
    return send


def element_screenshot(pw: Playwright, page: Page, tr: TestRow, logs: Logs):
    logs.log.info(f"(ActionFunctions/page_screenshot) {vars(tr)}")

    logs.code_prog.info(
        f"page.wait_for_load_state(\"load\")\nelement = page.locator(\"{tr.locator}\")\nelement.screenshot(path=f\"{logs.directory_path}\\elescrnsht{time.strftime('%H%M%S')}{tr.filepath}\")")
    page.wait_for_load_state("load")
    element = page.locator(tr.locator)
    element.screenshot(path=f"{logs.directory_path}\\elescrnsht{time.strftime('%H%M%S')}{tr.filepath}")
    send = {'page': page}
    return send


def create_links_html(ref_loop_dict: dict, string, logs: Logs):
    logs.log.info(f"CreateLinksHTML/create_links_html) {string} {ref_loop_dict}")

    links_list = list(filter(lambda item: string in item[0], ref_loop_dict.items()))

    i = 1
    links_string = ""
    for value in links_list:
        links_string += f"<a id='{i}' href=\"{value[1]}\"> [Link #{i}: {value[1]}]</a>"
        i += 1
    print(links_string)

    html_code = (f"<!DOCTYPE html><html><head><title>Links HTML</title></head><body><p>Test Links:</p>"
                 f"{links_string}</body></html>")
    with open(f"../Html Pages/{string}.html", "w") as html_file:
        html_file.write(html_code)

    send = {'html_code': html_code}
    return send
