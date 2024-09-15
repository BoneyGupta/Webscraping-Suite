from playwright.sync_api import Page, Playwright, BrowserContext, expect

from entity.ExcelData import TestRow
from service.Logger import Logs


def open_link_in_new_tab(pw: Playwright, page: Page, url: str, logs: Logs):
    logs.log.info(f"(WindowHandler/open_link_in_new_tab) {url}")
    logs.code_prog.info(f"#Open link in new tab\npage.context.new_page().goto(url)\nnew_window.bring_to_front()")
    new_window = page.context.new_page()
    new_window.goto(url)
    new_window.bring_to_front()
    send = {'page': page}
    return send


def open_link_in_new_tab_from_element(pw: Playwright, page: Page, element, logs: Logs):
    logs.log.info(f"(WindowHandler/open_link_in_new_tab_from_element) {element}")
    msg = f"# Open link in new tab from element"
    logs.code_prog.info(msg)
    all_before = page.context.pages
    all_after = all_before
    # print("clicking: " + element.text_content())
    element.click()
    temp_page = page.context.new_page()
    temp_page.goto("https://www.google.com")

    while len(all_after) <= (len(all_before) + 1):
        all_after = page.context.pages
    temp_page.close()
    pgs = page.context.pages
    p: Page = pgs[0]
    # print("Pages open:")
    for p in pgs:
        # print(p.title())
        p.bring_to_front()
    send = {'page': p}
    return send


def goto_parent_tab(pw: Playwright, page: Page, logs: Logs):
    logs.log.info(f"(WindowHandler/goto_parent_tab)")
    logs.code_prog.info(f"page.context.pages[0].bring_to_front()")
    total_pages = page.context.pages
    total_pages[0].bring_to_front()
    send = {'page': page}
    return send


def close_tab(pw: Playwright, page: Page, logs: Logs):
    logs.log.info(f"(WindowHandler/close_tab)")
    logs.code_prog.info(f"page.close()")
    page.close()
    receive = goto_parent_tab(pw, page, logs)
    page = receive['page']
    send = {'page': page}
    return send


def goto_url(pw: Playwright, page: Page, tr: TestRow, logs: Logs):
    logs.log.info(f"(ActionFunctions/goto_url) {vars(tr)}")
    logs.code_prog.info(f"page.goto(\"{tr.url}\")\npage.wait_for_load_state('load')")
    page.goto(tr.url)
    page.wait_for_load_state('load')

    send = {'page': page}
    return send
