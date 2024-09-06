import os

from playwright.sync_api import Playwright, sync_playwright, Page, Browser, BrowserContext
from entity.ExcelData import TestDetails


def select_browser(pw: Playwright, brwsr: str, headless: bool, cdp: bool):
    # To connect to an already running browser (Chrome) session, you can use connect_over_cdp method (added in v1.9 of
    # playwright). For this, you need to start Chrome in debug mode. Create a desktop shortcut for Chrome and edit
    # Target section of shortcut properties to start it with debug mode. Add --remote-debugging-port=9222 to the target
    # box in shortcut properties so that the target path becomes: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 Now start Chrome and check if it is in
    # debug mode. For this open a new tab and paste this url in the address bar: http://localhost:9222/json/version. If
    # you are in debug mode, you should see now a page with a json response, otherwise if you are in "normal" mode,
    # it will say "Page not found" or something similar.
    #
    if cdp:
        return pw.chromium.connect_over_cdp("http://localhost:9988")
    if "chrom" in brwsr:
        browser = pw.chromium.launch(headless=headless)
    elif "edge" in brwsr:
        browser = pw.chromium.launch(headless=headless)
    elif "fire" in brwsr or "gecko" in brwsr:
        browser = pw.firefox.launch(headless=headless)
    else:
        print("Browser selection is incorrect. Continuing with Chrome")
        browser = pw.chromium.launch(headless=headless)

    return browser


def open_browser_context(browser: Browser, cdp: bool):
    if cdp:
        return browser.contexts[0]
    return browser.new_context()


def open_page(context: BrowserContext, cdp: bool):
    if cdp:
        return context.pages[0]
    return context.new_page()


def close_page(page: Page):
    page.close()


def close_browser_context(context: BrowserContext):
    context.close()


def close_browser(browser: Browser):
    browser.close()


def open_browser_in_debugging_mode():
    cwd = "Application"
    command = "chrome.exe --remote-debugging-port=9988 --user-data-dir=..\\chromedata"
    try:
        os.chdir(cwd) if cwd else None
        result = os.system(command)
        if result == 0:
            print("Command executed successfully.")
        else:
            print(f"Command failed with error code {result}.")
    except OSError as e:
        print(f"Error running command: {e}")

    os.system("exit")


def fresh_browser(pw: Playwright, page: Page, headless, master_url):
    if master_url == "":
        master_url = page.url
    browser = pw.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()
    page.goto(master_url)
    send = {'page': page}
    return send
