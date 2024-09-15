import os
import threading
import time

from playwright.sync_api import Playwright, sync_playwright


def open_browser():
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


def run(pw: Playwright) -> None:
    print("Start Test")

    t: threading
    t = threading.Thread(target=open_browser)
    t.start()
    t.join(timeout=5)
    os.chdir('..')

    browser = pw.chromium.connect_over_cdp("http://localhost:9988")
    context = browser.contexts[0]
    page = context.pages[0]

    page.goto("https://web.whatsapp.com")
    page.wait_for_load_state("load")
    time.sleep(20)
    page.locator("//div[@role='textbox']").click()
    page.locator("//div[@role='textbox']").fill("Aaryaman")
    page.locator("//div[@role='textbox']").press("Enter")
    page.keyboard.type("Hello")
    page.keyboard.press("Enter")

    page.keyboard.press("Escape")

    page.locator("//div[@role='textbox']").click()
    page.locator("//div[@role='textbox']").fill("Vaibhav")
    page.locator("//div[@role='textbox']").press("Enter")
    page.keyboard.type("Automatic Hello")
    page.keyboard.press("Enter")
    time.sleep(10)
    page.close()


start_time = time.time()

with sync_playwright() as playwright:
    run(playwright)

run(sync_playwright())

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
