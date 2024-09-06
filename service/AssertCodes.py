from playwright.sync_api import Playwright, Page, expect

from entity.ExcelData import TestRow
from service.Logger import Logs


def execute_assert_code(pw: Playwright, page: Page, tr: TestRow, assert_code, logs: Logs):
    logs.log.info(f"(ActionFunctions/execute_assert_code) {vars(tr)}, {assert_code}")

    exec_str = assert_code

    if 'hard' in tr.assertion.lower():
        try:
            logs.code_prog.info(exec_str)
            exec(exec_str)
        except Exception as e:
            print(f"Error: {str(e)}")
        exec(exec_str)
        send = {'page': page, 'pass': True, 'message': "All OK"}
        return send

    elif 'soft' in tr.assertion.lower():
        try:
            logs.code_prog.info(exec_str)
            exec(exec_str)
            send = {'page': page, 'pass': True, 'message': "All OK"}
        except Exception as e:
            # page.screenshot(path=f"{logs.directory_path}/screenshot-eaue-{time.strftime("%Y-%m-%d %H%M%S")}.png",timeout=100000)
            print(f"Error: {str(e)}")
            send = {'page': page, 'pass': False, 'message': f"Error: {str(e)}"}
        return send

    send = {'page': page, 'pass': True, 'message': "Did not run assert"}
    return send


def execute_assert_using_element(pw: Playwright, page: Page, tr: TestRow, assert_code, logs: Logs):
    logs.log.info(f"(ActionFunctions/execute_module) {vars(tr)},{assert_code}")

    exec_str = assert_code

    if 'hard' in tr.assertion.lower():
        try:
            logs.code_prog.info(exec_str)
            exec(exec_str)
        except Exception as e:
            print(f"Error: {str(e)}")
        exec(exec_str)
        send = {'page': page, 'pass': True, 'message': "All OK"}
        return send
    elif 'soft' in tr.assertion.lower():
        try:
            logs.code_prog.info(exec_str)
            exec(exec_str)
            send = {'page': page, 'pass': True, 'message': "All OK"}
        except Exception as e:
            # page.screenshot(path=f"{logs.directory_path}/screenshot-eaue-{time.strftime("%Y-%m-%d %H%M%S")}.png", timeout=100000)
            print(f"Error: {str(e)}")
            send = {'page': page, 'pass': False, 'message': f"Error: {str(e)}"}
        return send

    send = {'page': page, 'pass': True, 'message': "Did not run assert using elements"}
    return send
