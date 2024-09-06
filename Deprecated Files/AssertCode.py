# import time
#
# from playwright.sync_api import Playwright, Page, expect
#
# from entity.ExcelData import TestRow
# from service.Logger import Logs
#
#
# def assert_code(page: Page, tr: TestRow, logs: Logs):
#     logs.log.info(f"Inside assert_code: {vars(tr)}")
#     code_dict = {
#         'to be attached': f"expect(page.locator(\"{tr.locator}\").first,\"element not present in page/dynamic element\").to_be_attached()",
#         'to be checked': f"expect(page.locator(\"{tr.locator}\").first,\"element is not checked\").to_be_checked()",
#         'to be disabled': f"expect(page.locator(\"{tr.locator}\").first,\"element is not disabled\").to_be_disabled()",
#         'to be editable': f"expect(page.locator(\"{tr.locator}\").first,\"element is not editable\").to_be_editable()",
#         'to be empty': f"expect(page.locator(\"{tr.locator}\").first,\"element is not empty\").to_be_empty()",
#         'to be enabled': f"expect(page.locator(\"{tr.locator}\").first,\"element is not enabled\").to_be_enabled()",
#         'to be focused': f"expect(page.locator(\"{tr.locator}\").first,\"element is not focused\").to_be_focused()",
#         'to be hidden': f"expect(page.locator(\"{tr.locator}\").first,\"element is not hidden\").to_be_hidden()",
#         'to be in viewport': f"expect(page.locator(\"{tr.locator}\").first,\"element is not in viewport\").to_be_in_viewport()",
#         'to be visible': f"expect(page.locator(\"{tr.locator}\").first,\"element is not visible\").to_be_visible()",
#         'to contain text': f"expect(page.locator(\"{tr.locator}\").first,\"element does not contain text\").to_contain_text(\"{tr.assertvalue}\")",
#         'to have accessible description': f"expect(page.locator(\"{tr.locator}\").first,\"element does not have accessible description\").to_have_accessible_description(\"{tr.assertvalue}\")",
#         'to have accessible name': f"expect(page.locator(\"{tr.locator}\").first,\"element does not have accessible name\").to_have_accessible_name(\"{tr.assertvalue}\")",
#         'to have attribute': f"expect(page.locator(\"{tr.locator}\").first,\"element is not empty\").to_have_attribute({tr.assertvalue})",
#         'to have class': f"expect(page.locator(\"{tr.locator}\").first,\"element does not have class\").to_have_class(\"{tr.assertvalue}\")",
#         'to have count': f"expect(page.locator(\"{tr.locator}\").first,\"element does not have count\").to_have_count(\"{tr.assertvalue}\")",
#         'to have css': f"expect(page.locator(\"{tr.locator}\").first,\"element does not have css\").to_have_css(\"{tr.assertvalue}\")",
#         'to have id': f"expect(page.locator(\"{tr.locator}\").first,\"element does not have id\").to_have_id(\"{tr.assertvalue}\")",
#         'to have js property': f"expect(page.locator(\"{tr.locator}\").first,\"element does not have the js properties\").to_have_js_property({tr.assertvalue})",
#         'to have role': f"expect(page.locator(\"{tr.locator}\").first,\"element does not have the role\").to_have_role(\"{tr.assertvalue}\")",
#         'to have text': f"expect(page.locator(\"{tr.locator}\").first,\"element does not have the text\").to_have_text(\"{tr.assertvalue}\")",
#         'to have value': f"expect(page.locator(\"{tr.locator}\").first,\"element does not have the value\").to_have_value(\"{tr.assertvalue}\")",
#         'to have values': f"expect(page.locator(\"{tr.locator}\").first,\"element do not have the values \").to_have_values([{tr.assertvalue}])",
#         'to have title': f"expect(\"{page}\",\"page does not have title\").to_have_title(\"{tr.assertvalue}\")",
#         'to have url': f"expect(\"{page}\",\"page does not have url\").to_have_url(\"{tr.assertvalue}\")",
#         'to be ok': f"expect(page.locator(\"{tr.locator}\").first,\"element is not ok\").to_be_ok()",
#
#         'not to be attached': f"expect(page.locator(\"{tr.locator}\").first,\"element is present in page/dynamic element\").not_to_be_attached()",
#         'not to be checked': f"expect(page.locator(\"{tr.locator}\").first,\"element is checked\").not_to_be_checked()",
#         'not to be disabled': f"expect(page.locator(\"{tr.locator}\").first,\"element is disabled\").not_to_be_disabled()",
#         'not to be editable': f"expect(page.locator(\"{tr.locator}\").first,\"element is editable\").not_to_be_editable()",
#         'not to be empty': f"expect(page.locator(\"{tr.locator}\").first,\"element is empty\").not_to_be_empty()",
#         'not to be enabled': f"expect(page.locator(\"{tr.locator}\").first,\"element is enabled\").not_to_be_enabled()",
#         'not to be focused': f"expect(page.locator(\"{tr.locator}\").first,\"element is focused\").not_to_be_focused()",
#         'not to be hidden': f"expect(page.locator(\"{tr.locator}\").first,\"element is hidden\").not_to_be_hidden()",
#         'not to be in viewport': f"expect(page.locator(\"{tr.locator}\").first,\"element is in viewport\").not_to_be_in_viewport()",
#         'not to be visible': f"expect(page.locator(\"{tr.locator}\").first,\"element is visible\").not_to_be_visible()",
#         'not to contain text': f"expect(page.locator(\"{tr.locator}\").first,\"element contains text\").not_to_contain_text(\"{tr.assertvalue}\")",
#         'not to have accessible description': f"expect(page.locator(\"{tr.locator}\").first,\"element has accessible description\").not_to_have_accessible_description(\"{tr.assertvalue}\")",
#         'not to have accessible name': f"expect(page.locator(\"{tr.locator}\").first,\"element has accessible name\").not_to_have_accessible_name(\"{tr.assertvalue}\")",
#         'not to have attribute': f"expect(page.locator(\"{tr.locator}\").first,\"element has attribute\").not_to_have_attribute({tr.assertvalue})",
#         'not to have class': f"expect(page.locator(\"{tr.locator}\").first,\"element has class\").not_to_have_class(\"{tr.assertvalue}\")",
#         'not to have count': f"expect(page.locator(\"{tr.locator}\").first,\"element has count\").not_to_have_count({tr.assertvalue})",
#         'not to have css': f"expect(page.locator(\"{tr.locator}\").first,\"element has css\").not_to_have_css(\"{tr.assertvalue}\")",
#         'not to have id': f"expect(page.locator(\"{tr.locator}\").first,\"element has id\").not_to_have_id(\"{tr.assertvalue}\")",
#         'not to have js property': f"expect(page.locator(\"{tr.locator}\").first,\"element has the js properties\").not_to_have_js_property({tr.assertvalue})",
#         'not to have role': f"expect(page.locator(\"{tr.locator}\").first,\"element has the role\").not_to_have_role(\"{tr.assertvalue}\")",
#         'not to have text': f"expect(page.locator(\"{tr.locator}\").first,\"element has the text\").not_to_have_text(\"{tr.assertvalue}\")",
#         'not to have value': f"expect(page.locator(\"{tr.locator}\").first,\"element has value\").not_to_have_value(\"{tr.assertvalue}\")",
#         'not to have values': f"expect(page.locator(\"{tr.locator}\").first,\"element has values \").not_to_have_values([{tr.assertvalue}])",
#         'not to have title': f"expect(\"{page}\",\"page has title\").not_to_have_title(\"{tr.assertvalue}\")",
#         'not to have url': f"expect(\"{page}\",\"page has url\").not_to_have_url(\"{tr.assertvalue}\")",
#         'not to be ok': f"expect(page.locator(\"{tr.locator}\").first,\"element is ok\").not_to_be_ok()"
#     }
#     print(code_dict[tr.condition])
#     send = {'code': code_dict[tr.condition]}
#     return send
#
#
# def assert_to_be_attached(pw: Playwright, page: Page, element, tr: TestRow, logs: Logs):
#     logs.log.info(f"Inside assert_to_be_attached: {vars(tr)}, {element}")
#
#     send = {'page': page, 'pass': True, 'message': "Assertion not available"}
#     if 'soft' in tr.assertion.lower():
#         try:
#             logs.code_prog.info(f"expect({element}, \"element is not attached\").to_be_attached()")
#             expect(element, "element is not attached").to_be_attached()
#             send = {'page': page, 'pass': True, 'message': "All OK"}
#         except Exception as e:
#             # page.screenshot(path=f"{logs.directory_path}/screenshot-atba-{time.strftime("%Y-%m-%d %H%M%S")}.png",
#             #                 timeout=100000)
#             print(f"Error: {str(e)}")
#             send = {'page': page, 'pass': False, 'message': f"Error: {str(e)}"}
#     elif 'hard' in tr.assertion.lower():
#         try:
#             logs.code_prog.info(f"expect({element}, \"element is not attached\").to_be_attached()")
#             expect(element, "element is not attached").to_be_attached()
#         except Exception as e:
#             print(f"Error: {str(e)}")
#         expect(element, "element is not ok").to_be_ok()
#         send = {'page': page, 'pass': True, 'message': "All OK"}
#     return send
#
#
# def assert_code_using_element(pw: Playwright, page: Page, tr: TestRow, logs: Logs):
#     logs.log.info(f"Inside assert_code_using_element: {vars(tr)}")
#
#     code_dict = {
#         'to be attached': f"expect(element,\"element not present in page/dynamic element\").to_be_attached()",
#         'to be checked': f"expect(element,\"element is not checked\").to_be_checked()",
#         'to be disabled': f"expect(element,\"element is not disabled\").to_be_disabled()",
#         'to be editable': f"expect(element,\"element is not editable\").to_be_editable()",
#         'to be empty': f"expect(element,\"element is not empty\").to_be_empty()",
#         'to be enabled': f"expect(element,\"element is not enabled\").to_be_enabled()",
#         'to be focused': f"expect(element,\"element is not focused\").to_be_focused()",
#         'to be hidden': f"expect(element,\"element is not hidden\").to_be_hidden()",
#         'to be in viewport': f"expect(element,\"element is not in viewport\").to_be_in_viewport()",
#         'to be visible': f"expect(element,\"element is not visible\").to_be_visible()",
#         'to contain text': f"expect(element,\"element does not contain text\").to_contain_text(\"{tr.assertvalue}\")",
#         'to have accessible description': f"expect(element,\"element does not have accessible description\").to_have_accessible_description(\"{tr.assertvalue}\")",
#         'to have accessible name': f"expect(element,\"element does not have accessible name\").to_have_accessible_name(\"{tr.assertvalue}\")",
#         'to have attribute': f"expect(element,\"element is not empty\").to_have_attribute({tr.assertvalue})",
#         'to have class': f"expect(element,\"element does not have class\").to_have_class(\"{tr.assertvalue}\")",
#         'to have count': f"expect(element,\"element does not have count\").to_have_count(\"{tr.assertvalue}\")",
#         'to have css': f"expect(element,\"element does not have css\").to_have_css(\"{tr.assertvalue}\")",
#         'to have id': f"expect(element,\"element does not have id\").to_have_id(\"{tr.assertvalue}\")",
#         'to have js property': f"expect(element,\"element does not have the js properties\").to_have_js_property({tr.assertvalue})",
#         'to have role': f"expect(element,\"element does not have the role\").to_have_role(\"{tr.assertvalue}\")",
#         'to have text': f"expect(element,\"element does not have the text\").to_have_text(\"{tr.assertvalue}\")",
#         'to have value': f"expect(element,\"element does not have the value\").to_have_value(\"{tr.assertvalue}\")",
#         'to have values': f"expect(element,\"element do not have the values \").to_have_values([{tr.assertvalue}])",
#         'to have title': f"expect(\"{page}\",\"page does not have title\").to_have_title(\"{tr.assertvalue}\")",
#         'to have url': f"expect(\"{page}\",\"page does not have url\").to_have_url(\"{tr.assertvalue}\")",
#         'to be ok': f"expect(element,\"element is not ok\").to_be_ok()",
#
#         'not to be attached': f"expect(element,\"element is present in page/dynamic element\").not_to_be_attached()",
#         'not to be checked': f"expect(element,\"element is checked\").not_to_be_checked()",
#         'not to be disabled': f"expect(element,\"element is disabled\").not_to_be_disabled()",
#         'not to be editable': f"expect(element,\"element is editable\").not_to_be_editable()",
#         'not to be empty': f"expect(element,\"element is empty\").not_to_be_empty()",
#         'not to be enabled': f"expect(element,\"element is enabled\").not_to_be_enabled()",
#         'not to be focused': f"expect(element,\"element is focused\").not_to_be_focused()",
#         'not to be hidden': f"expect(element,\"element is hidden\").not_to_be_hidden()",
#         'not to be in viewport': f"expect(element,\"element is in viewport\").not_to_be_in_viewport()",
#         'not to be visible': f"expect(element,\"element is visible\").not_to_be_visible()",
#         'not to contain text': f"expect(element,\"element contains text\").not_to_contain_text(\"{tr.assertvalue}\")",
#         'not to have accessible description': f"expect(element,\"element has accessible description\").not_to_have_accessible_description(\"{tr.assertvalue}\")",
#         'not to have accessible name': f"expect(element,\"element has accessible name\").not_to_have_accessible_name(\"{tr.assertvalue}\")",
#         'not to have attribute': f"expect(element,\"element has attribute\").not_to_have_attribute({tr.assertvalue})",
#         'not to have class': f"expect(element,\"element has class\").not_to_have_class(\"{tr.assertvalue}\")",
#         'not to have count': f"expect(element,\"element has count\").not_to_have_count({tr.assertvalue})",
#         'not to have css': f"expect(element,\"element has css\").not_to_have_css(\"{tr.assertvalue}\")",
#         'not to have id': f"expect(element,\"element has id\").not_to_have_id(\"{tr.assertvalue}\")",
#         'not to have js property': f"expect(element,\"element has the js properties\").not_to_have_js_property({tr.assertvalue})",
#         'not to have role': f"expect(element,\"element has the role\").not_to_have_role(\"{tr.assertvalue}\")",
#         'not to have text': f"expect(element,\"element has the text\").not_to_have_text(\"{tr.assertvalue}\")",
#         'not to have value': f"expect(element,\"element has value\").not_to_have_value(\"{tr.assertvalue}\")",
#         'not to have values': f"expect(element,\"element has values \").not_to_have_values([{tr.assertvalue}])",
#         'not to have title': f"expect(\"{page}\",\"page has title\").not_to_have_title(\"{tr.assertvalue}\")",
#         'not to have url': f"expect(\"{page}\",\"page has url\").not_to_have_url(\"{tr.assertvalue}\")",
#         'not to be ok': f"expect(element,\"element is ok\").not_to_be_ok()"
#     }
#     print(code_dict[tr.condition])
#     send = {'code': code_dict[tr.condition]}
#     return send
