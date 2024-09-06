# import time
#
# from playwright.sync_api import Playwright, sync_playwright, Page, expect, Browser, BrowserContext
#
# from entity.ExcelData import TestRow
# from service.AssertCode import assert_code, assert_code_using_element
# from service.Logger import Logs
#
#
# def execute_code(pw: Playwright, page: Page, exec_str: str, logs: Logs):
#     logs.log.info(f"Inside execute_code: {exec_str}")
#     logs.code_prog.info(exec_str)
#     exec(exec_str)
#     return page
#
#
# def execute_code_get_data(pw: Playwright, page: Page, tr: TestRow, logs: Logs):
#     logs.log.info(f"Inside execute_code_get_data: {vars(tr)}")
#     if tr.timeout == "":
#         tr.timeout = 3000
#     if "text content" in tr.action:
#         logs.code_prog.info(f"data = page.wait_for_selector({tr.locator}, timeout={tr.timeout}).text_content()")
#         page.locator(tr.locator).first.wait_for(timeout=tr.timeout)
#         data = page.locator(tr.locator).first.text_content()
#     elif "all inner texts" in tr.action:
#         logs.code_prog.info(
#             f"page.wait_for_selector({tr.locator}, timeout={tr.timeout})\ndata = page.locator({tr.locator}).all_inner_texts()")
#         page.locator(tr.locator).first.wait_for(timeout=tr.timeout)
#         data = page.locator(tr.locator).first.all_inner_texts()
#     elif "all text contents" in tr.action:
#         logs.code_prog.info(
#             f"page.wait_for_selector({tr.locator}, timeout={tr.timeout})\ndata = page.locator({tr.locator}).all_text_contents()")
#         page.locator(tr.locator).first.wait_for(timeout=tr.timeout)
#         data = page.locator(tr.locator).first.all_text_contents()
#     elif "get page url" in tr.action:
#         logs.code_prog.info(f"data = page.url")
#         data = page.url
#     else:
#         data = ""
#
#     send = {'page': page, 'data': data}
#     return send['data']
#
#
# def execute_code_get_data_2(pw: Playwright, page: Page, exec_str: str, logs: Logs):
#     data = ""
#     logs.log.info(f"Inside execute_code_get_data: {exec_str}")
#     logs.code_prog.info(f"data = {exec_str}")
#     exec("data = " + exec_str)
#     send = {'page': page, "data": data}
#     return send['data']
#
#
# def execute_assert_code(pw: Playwright, page: Page, tr: TestRow, logs: Logs):
#     logs.log.info(f"Inside execute_assert_code: {vars(tr)}")
#     data = assert_code(page, tr, logs)
#     exec_str = data['code']
#
#     if 'hard' in tr.assertion.lower():
#         try:
#             logs.code_prog.info(exec_str)
#             exec(exec_str)
#         except Exception as e:
#             print(f"Error: {str(e)}")
#         exec(exec_str)
#         send = {'page': page, 'pass': True, 'message': "All OK"}
#         return send
#
#     elif 'soft' in tr.assertion.lower():
#         try:
#             logs.code_prog.info(exec_str)
#             exec(exec_str)
#             send = {'page': page, 'pass': True, 'message': "All OK"}
#         except Exception as e:
#             # page.screenshot(path=f"{logs.directory_path}/screenshot-eaue-{time.strftime("%Y-%m-%d %H%M%S")}.png",
#             #                 timeout=100000)
#             print(f"Error: {str(e)}")
#             send = {'page': page, 'pass': False, 'message': f"Error: {str(e)}"}
#         return send
#
#     send = {'page': page, 'pass': True, 'message': "Did not run assert"}
#     return send
#
#
# def execute_assert_using_element(pw: Playwright, page: Page, tr: TestRow, element, logs: Logs):
#     logs.log.info(f"Inside execute_module: {vars(tr)},{element}")
#     data = assert_code_using_element(pw, page, tr, logs)
#     exec_str = data['code']
#
#     if 'hard' in tr.assertion.lower():
#         try:
#             logs.code_prog.info(exec_str)
#             exec(exec_str)
#         except Exception as e:
#             print(f"Error: {str(e)}")
#         exec(exec_str)
#         send = {'page': page, 'pass': True, 'message': "All OK"}
#         return send
#     elif 'soft' in tr.assertion.lower():
#         try:
#             logs.code_prog.info(exec_str)
#             exec(exec_str)
#             send = {'page': page, 'pass': True, 'message': "All OK"}
#         except Exception as e:
#             # page.screenshot(path=f"{logs.directory_path}/screenshot-eaue-{time.strftime("%Y-%m-%d %H%M%S")}.png",
#             #                 timeout=100000)
#             print(f"Error: {str(e)}")
#             send = {'page': page, 'pass': False, 'message': f"Error: {str(e)}"}
#         return send
#
#     send = {'page': page, 'pass': True, 'message': "Did not run assert using elements"}
#     return send
