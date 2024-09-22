import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from entity.ExcelData import TestRow
from service.Logger import Logs


def execute_assert_code(driver, tr: TestRow, assert_code, logs: Logs):
    logs.log.info(f"(ActionFunctions/execute_assert_code) {vars(tr)}, {assert_code}")

    exec_str = assert_code

    if 'hard' in tr.assertion.lower():
        try:
            logs.code_prog.info(exec_str)
            exec(exec_str)
        except Exception as e:
            print(f"Error: {str(e)}")
        exec(exec_str)
        send = {'driver': driver, 'pass': True, 'message': "All OK"}
        return send

    elif 'soft' in tr.assertion.lower():
        try:
            logs.code_prog.info(exec_str)
            exec(exec_str)
            send = {'driver': driver, 'pass': True, 'message': "All OK"}
        except Exception as e:
            driver.save_screenshot(f"{logs.directory_path}/screenshot-eaue-{time.strftime('%Y-%m-%d %H%M%S')}.png")
            print(f"Error: {str(e)}")
            send = {'driver': driver, 'pass': False, 'message': f"Error: {str(e)}"}
        return send

    send = {'driver': driver, 'pass': True, 'message': "Did not run assert"}
    return send


def execute_assert_using_element(driver, tr: TestRow, assert_code, logs: Logs):
    logs.log.info(f"(ActionFunctions/execute_module) {vars(tr)},{assert_code}")

    exec_str = assert_code

    if 'hard' in tr.assertion.lower():
        try:
            logs.code_prog.info(exec_str)
            exec(exec_str)
        except Exception as e:
            print(f"Error: {str(e)}")
        exec(exec_str)
        send = {'driver': driver, 'pass': True, 'message': "All OK"}
        return send
    elif 'soft' in tr.assertion.lower():
        try:
            logs.code_prog.info(exec_str)
            exec(exec_str)
            send = {'driver': driver, 'pass': True, 'message': "All OK"}
        except Exception as e:
            driver.save_screenshot(f"{logs.directory_path}/screenshot-eaue-{time.strftime('%Y-%m-%d %H%M%S')}.png")
            print(f"Error: {str(e)}")
            send = {'driver': driver, 'pass': False, 'message': f"Error: {str(e)}"}
        return send

    send = {'driver': driver, 'pass': True, 'message': "Did not run assert using elements"}
    return send
