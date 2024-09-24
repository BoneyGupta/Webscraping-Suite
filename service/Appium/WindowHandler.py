from appium import webdriver
from entity.ExcelData import TestRow
from service.Logger import Logs


def open_link_in_new_tab(driver: webdriver.Remote, url: str, logs: Logs):
    logs.log.info(f"(WindowHandler/open_link_in_new_tab) {url}")
    logs.code_prog.info(f"# Open link in new tab")

    driver.execute_script("window.open(arguments[0]);", url)  # Opens the URL in a new tab
    driver.switch_to.window(driver.window_handles[-1])  # Switches to the new tab
    send = {'driver': driver}
    return send


def open_link_in_new_tab_from_element(driver: webdriver.Remote, element, logs: Logs):
    logs.log.info(f"(WindowHandler/open_link_in_new_tab_from_element) {element.text}")
    logs.code_prog.info(f"# Open link in new tab from element")

    element.click()
    driver.execute_script("window.open('https://www.google.com');")  # Opens a new tab
    driver.switch_to.window(driver.window_handles[-1])  # Switches to the new tab

    send = {'driver': driver}
    return send


def goto_parent_tab(driver: webdriver.Remote, logs: Logs):
    logs.log.info(f"(WindowHandler/goto_parent_tab)")
    logs.code_prog.info(f"Switching to the parent tab")

    driver.switch_to.window(driver.window_handles[0])  # Switch to the first tab
    send = {'driver': driver}
    return send


def close_tab(driver: webdriver.Remote, logs: Logs):
    logs.log.info(f"(WindowHandler/close_tab)")
    logs.code_prog.info(f"Closing current tab")

    driver.close()  # Closes the current tab
    goto_parent_tab(driver, logs)  # Switch back to the parent tab

    send = {'driver': driver}
    return send


def goto_url(driver: webdriver.Remote, tr: TestRow, logs: Logs):
    logs.log.info(f"(ActionFunctions/goto_url) {vars(tr)}")
    logs.code_prog.info(f"driver.get(\"{tr.url}\")")

    driver.get(tr.url)  # Navigates to the URL
    # You might want to add an explicit wait here to ensure the page loads
    # Example: WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    send = {'driver': driver}
    return send
