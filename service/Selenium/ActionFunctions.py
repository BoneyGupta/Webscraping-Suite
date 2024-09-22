import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from entity.ExcelData import TestRow
from service.Logger import Logs


def execute_code_get_data(driver, tr: TestRow, logs: Logs):
    logs.log.info(f"(ActionFunctions/execute_code_get_data) {vars(tr)}")

    # Variables
    data = ""

    # Process Locator
    locator = tr.locator.replace("\"", "\'")

    # Process Timeout
    timeout = tr.timeout
    if tr.timeout == "":
        timeout = 3  # Selenium timeout in seconds

    # Process nth
    nth = tr.nth
    if tr.nth == "":
        nth = 0

    # Process assertion
    assertion = tr.assertion.lower()

    if tr.action == "get attribute":
        logs.code_prog.info(
            f"data = driver.find_elements(By.XPATH, \"{locator}\")[{nth}].get_attribute(\"{tr.value}\")")
        data = driver.find_elements(By.XPATH, locator)[nth].get_attribute(tr.value)
    elif tr.action == "is checked":
        logs.code_prog.info(f"data = driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_selected()")
        data = driver.find_elements(By.XPATH, locator)[nth].is_selected()
    elif tr.action == "is disabled":
        logs.code_prog.info(f"data = not driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_enabled()")
        data = not driver.find_elements(By.XPATH, locator)[nth].is_enabled()
    elif tr.action == "is visible":
        logs.code_prog.info(f"data = driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_displayed()")
        data = driver.find_elements(By.XPATH, locator)[nth].is_displayed()
    elif tr.action == "is hidden":
        logs.code_prog.info(f"data = not driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_displayed()")
        data = not driver.find_elements(By.XPATH, locator)[nth].is_displayed()
    elif tr.action == "is enabled":
        logs.code_prog.info(f"data = driver.find_elements(By.XPATH, \"{locator}\")[{nth}].is_enabled()")
        data = driver.find_elements(By.XPATH, locator)[nth].is_enabled()
    elif tr.action == "wait for":
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
    elif tr.action == "wait for element state":
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
    elif tr.action == "screenshot":
        driver.save_screenshot(f"{logs.directory_path}/pgscrnsht{time.strftime('%H%M%S')}{tr.filepath}")
    elif tr.action == "bounding box":
        element = driver.find_elements(By.XPATH, locator)[nth]
        data = element.size
    elif tr.action == "with text":
        pass
    elif tr.action == "count":
        logs.code_prog.info(f"data = len(driver.find_elements(By.XPATH, \"{locator}\"))")
        data = len(driver.find_elements(By.XPATH, locator))
    elif tr.action == "inner text":
        logs.code_prog.info(f"data = driver.find_elements(By.XPATH, \"{locator}\")[{nth}].text")
        data = driver.find_elements(By.XPATH, locator)[nth].text
    elif tr.action == "text content":
        logs.code_prog.info(f"data = driver.find_elements(By.XPATH, \"{locator}\")[{nth}].text")
        data = driver.find_elements(By.XPATH, locator)[nth].text
    elif tr.action == "all inner texts":
        logs.code_prog.info(f"data = [el.text for el in driver.find_elements(By.XPATH, \"{locator}\")]")
        data = [el.text for el in driver.find_elements(By.XPATH, locator)]
    elif tr.action == "all text contents":
        logs.code_prog.info(f"data = [el.text for el in driver.find_elements(By.XPATH, \"{locator}\")]")
        data = [el.text for el in driver.find_elements(By.XPATH, locator)]
    elif tr.action == "get page url":
        logs.code_prog.info(f"data = driver.current_url")
        data = driver.current_url
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

    send = {'driver': driver, 'data': data}
    return send


def execute_code(driver, tr: TestRow, exec_str: str, logs: Logs):
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

    send = {'driver': driver}
    return send


def page_screenshot(driver, tr: TestRow, logs: Logs):
    logs.log.info(f"(ActionFunctions/page_screenshot) {vars(tr)}")

    logs.code_prog.info(
        f"driver.save_screenshot(f\"{logs.directory_path}\\pgscrnsht{time.strftime('%H%M%S')}{tr.filepath}\")")
    driver.save_screenshot(f"{logs.directory_path}\\pgscrnsht{time.strftime('%H%M%S')}{tr.filepath}")
    send = {'driver': driver}
    return send


def element_screenshot(driver, tr: TestRow, logs: Logs):
    logs.log.info(f"(ActionFunctions/page_screenshot) {vars(tr)}")

    logs.code_prog.info(
        f"element = driver.find_element(By.XPATH, \"{tr.locator}\")\nelement.screenshot(f\"{logs.directory_path}\\elescrnsht{time.strftime('%H%M%S')}{tr.filepath}\")")
    element = driver.find_element(By.XPATH, tr.locator)
    element.screenshot(f"{logs.directory_path}\\elescrnsht{time.strftime('%H%M%S')}{tr.filepath}")
    send = {'driver': driver}
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
