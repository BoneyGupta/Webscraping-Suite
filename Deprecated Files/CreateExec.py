# from service.ActionFunctions import *
# from service.Logger import Logs
# from service.WindowHandler import *
#
#
# def create_element_obj(tr: TestRow, logs: Logs):
#     logs.log.info(f"Inside create_element_obj: {vars(tr)}")
#
#     tr.locator = tr.locator.replace("\"", "\'")
#     if tr.timeout == "":
#         tr.timeout = 3000
#     return f"page.locator(\"{tr.locator}\").first.wait_for(timeout={tr.timeout})\npage.locator(\"{tr.locator}\")"
#
#
# def create_exec_str(pw: Playwright, page: Page, tr: TestRow, element, logs: Logs):
#     logs.log.info(f"Inside create_exec_str: {vars(tr)}, {element}")
#
#     exec_created = True
#
#     code = ""
#     if "all inner texts" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.all_inner_texts()"
#     elif "all text contents" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.all_text_contents()"
#     elif "double click" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.double_click()"
#     elif "open in new tab" in tr.action:
#         exec_created = False
#         open_link_in_new_tab(pw, page, tr.url, logs)
#     elif "parent tab" in tr.action:
#         exec_created = False
#         goto_parent_tab(pw, page, logs)
#     elif "close tab" in tr.action:
#         exec_created = False
#         close_tab(pw, page, logs)
#     elif "loop new tab" in tr.action:
#         exec_created = False
#         page = open_link_in_new_tab_from_element(pw, page, element, logs)
#     elif "open link" in tr.action:
#         exec_created = False
#         open_url(pw, page, tr.url, logs)
#     elif "get page url" in tr.action:
#         code = "page.url"
#     elif "page screenshot" in tr.action:
#         exec_created = False
#         page_screenshot(pw, page, tr, logs)
#     elif "element screenshot" in tr.action:
#         exec_created = False
#         element_screenshot(pw, page, tr, logs)
#     elif "open url" in tr.action:
#         exec_created = False
#         receive = goto_url(pw, page, tr, logs)
#         page = receive['page']
#
#     elif "text content" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.text_content()"
#     elif "focus" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.focus()"
#     elif "hover" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.hover()"
#     elif "select options" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.select_options([{tr.value}])"
#     elif "select option" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.select_option(\"{tr.value}\")"
#
#     elif "click" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.click()"
#     elif "fill" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.fill(\"{tr.value}\")"
#     elif "press" in tr.action:
#         code = f"{create_element_obj(tr, logs)}.press(\"{tr.value}\")"
#
#     else:
#         code = create_element_obj(tr, logs)
#
#     send = {'page': page, 'code': code, 'exec_created': exec_created}
#     return send
