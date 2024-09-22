import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def select_browser(brwsr: str, headless: bool, cdp: bool):
    options = None
    driver = None

    # Handle browser selection
    if cdp:
        # Connecting to an already running browser with CDP
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    if "chrom" in brwsr:
        options = Options()
        options.headless = headless
        driver = webdriver.Chrome(options=options)
    elif "edge" in brwsr:
        # You can add edge specific options here if needed
        options = Options()
        options.headless = headless
        driver = webdriver.Edge(options=options)
    elif "fire" in brwsr or "gecko" in brwsr:
        options = FirefoxOptions()
        options.headless = headless
        driver = webdriver.Firefox(options=options)
    else:
        print("Browser selection is incorrect. Continuing with Chrome")
        options = Options()
        options.headless = headless
        driver = webdriver.Chrome(options=options)

    return driver


def open_browser_context(driver, cdp: bool):
    # In Selenium, there isn't a direct concept of browser contexts like in Playwright
    # Instead, you manage the driver instance and open pages in different tabs/windows if needed.
    if cdp:
        # In CDP mode, you are already connected to an existing browser
        return driver
    return driver


def open_page(driver, cdp: bool):
    if cdp:
        # In CDP, the current page is already open, so return the current session
        return driver
    return driver


def close_page(driver):
    driver.close()


def close_browser_context(driver):
    # In Selenium, this typically means quitting the driver instance
    driver.quit()


def close_browser(driver):
    driver.quit()


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


def fresh_browser(brwsr: str, headless: bool, master_url: str):
    if master_url == "":
        master_url = "about:blank"  # Default to a blank page if no URL is provided

    driver = select_browser(brwsr, headless, cdp=False)  # We do not use CDP in fresh browser

    driver.get(master_url)  # Open the provided URL in the new browser

    send = {'driver': driver}
    return send
