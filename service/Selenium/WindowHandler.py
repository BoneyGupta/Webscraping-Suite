from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from entity.ExcelData import TestRow
from service.Logger import Logs


def open_link_in_new_tab(driver, url: str, logs: Logs):
    logs.log.info(f"(WindowHandler/open_link_in_new_tab) {url}")
    logs.code_prog.info(
        f"# Open link in new tab\nnew_window = driver.execute_script('window.open(\"{url}\", \"_blank\");')")
    driver.execute_script("window.open(arguments[0], '_blank');", url)
    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])
    return {'page': driver}


def open_link_in_new_tab_from_element(driver, element, logs: Logs):
    logs.log.info(f"(WindowHandler/open_link_in_new_tab_from_element) {element.text}")
    msg = f"# Open link in new tab from element"
    logs.code_prog.info(msg)
    all_before = len(driver.window_handles)

    element.click()  # Click the element to open the link in a new tab
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > all_before)  # Wait for the new tab to open

    # Switch to the new tab
    new_tab = driver.window_handles[-1]
    driver.switch_to.window(new_tab)
    driver.get("https://www.google.com")  # Example of navigating to a new page

    # Optionally close the new tab and switch back
    driver.close()
    driver.switch_to.window(driver.window_handles[0])  # Switch back to the original tab

    return {'page': driver}


def goto_parent_tab(driver, logs: Logs):
    logs.log.info(f"(WindowHandler/goto_parent_tab)")
    logs.code_prog.info(f"Switching to the first tab")
    driver.switch_to.window(driver.window_handles[0])
    return {'page': driver}


def close_tab(driver, logs: Logs):
    logs.log.info(f"(WindowHandler/close_tab)")
    logs.code_prog.info(f"Closing current tab")
    driver.close()
    return goto_parent_tab(driver, logs)


def goto_url(driver, tr: TestRow, logs: Logs):
    logs.log.info(f"(ActionFunctions/goto_url) {vars(tr)}")
    logs.code_prog.info(f"driver.get(\"{tr.url}\")")
    driver.get(tr.url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Wait for the page to load

    return {'page': driver}
