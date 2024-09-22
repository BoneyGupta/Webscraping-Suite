import threading
import time
import os
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from entity.ExcelData import *
from service.ActionFunctions import *
from service.Selenium.AssertCodes import *
from service.Selenium.CodeCreate import *
from service.Logger import Logs
from utils import JsonHandler
from service.CreatelLinksHTML import create_links_html


class StartTest:
    data_dict: dict = {}
    ref_dict_loop: dict = {}
    ref_dict_loop_counter = 1
    ref_dict: dict = {}
    dictionary: dict = {}
    ref_counter: int = 1
    master_url = ""
    master_row = 0

    def __init__(self, xlwb: ExcelWorkBook, logs: Logs, browser_options=None):
        self.xlwb = xlwb
        self.logs = logs
        self.browser_options = browser_options

    def config(self, td):
        """
        Driver class for the Excel workbook test cases.
        Can only work with one excel workbook
        :return:
        """

        # Set up WebDriver
        options = webdriver.ChromeOptions()
        if self.browser_options:
            for option in self.browser_options:
                options.add_argument(option)
        service = ChromeService(executable_path='/path/to/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)

        url = td.website
        driver.get(url)  # Opens the website

        for i in range(self.xlwb.sheet_count):
            self.logs.log.info(f"Sheet loop number: {i}")
            if "test" in self.xlwb.sheet_names[i].lower():
                self.xlwb.change_sheet(i)
                try:
                    self.logs.log.info(f"** sheets: Entry Point #2 ** {self.xlwb.sheet_names[i]}")
                    self.sheets(driver, self.xlwb.sheet_names[i])
                    self.logs.log.info(f"** sheets: Exit Point #2 **")
                except Exception as e:
                    screenshot_file = f"{self.logs.directory_path}/screenshot-config-{time.strftime('%Y-%m-%d %H%M%S')}.png"
                    self.logs.log.critical(f"Sheet: {self.xlwb.sheet_names[i]}\n Screenshot: {screenshot_file}")
                    driver.save_screenshot(screenshot_file)
                    self.logs.log.error(f"{self.xlwb.sheet_names[i]} did not process complete. Continue with next test")
                    print(f"Error: {str(e)}")
                    self.logs.log.info(f"Error: {str(e)}")
                    raise
                finally:
                    JsonHandler.create_json_file(f"{self.logs.directory_path}/data{time.strftime('%H%M%S')}.json",
                                                 self.data_dict)
                    JsonHandler.create_json_file(
                        f"{self.logs.directory_path}/reference_data{time.strftime('%H%M%S')}.json", self.ref_dict)
                    JsonHandler.create_json_file(
                        f"{self.logs.directory_path}/ref_loop_data{time.strftime('%H%M%S')}.json", self.ref_dict_loop)

        driver.quit()

    def sheets(self, driver, sheet_name):
        print("Current testing: " + sheet_name)

        row = 3
        while row <= self.xlwb.get_rows_count():
            self.logs.log.info(f"Sheet row: {row}")

            tr = TestRow(self.xlwb, row)

            conditional_flag = False
            if tr.conditional_statement != "":
                receive = self.conditional_module(tr, self.dictionary, self.logs)
                if not receive['conditional_flag']:
                    conditional_flag = True

            if not conditional_flag and tr.conditional_statement != "":
                self.logs.log.info(f"Condition False for: {tr}")

            elif "master url" in tr.action:
                self.master_url = driver.current_url
                self.master_row = row
                self.logs.log.info(f"Master url and row allotted: {self.master_row}, {self.master_url}")

            elif "fresh browser" in tr.action:
                driver.quit()
                driver = webdriver.Chrome(service=ChromeService(executable_path='/path/to/chromedriver'),
                                          options=self.browser_options)
                driver.get(self.master_url)

            elif tr.action == "create html":
                create_links_html(self.ref_dict, tr.value, tr.filepath, self.logs)

            elif "start loop" in tr.description:
                self.logs.log.info(f"Start Loop Module(sheets): Entry Point #3 {vars(tr)},{row}")
                receive = self.start_loop_module(driver, tr, row)
                self.logs.log.info(f"Start Loop Module(sheets): Exit Point #3")
                row = receive['row']

            elif tr.execute != "":
                receive = self.execute_module(driver, tr, "")
                if tr.stored_value_key != "":
                    if receive['data_dict'] != {}:
                        self.data_dict[tr.stored_value_key] = receive['data_dict']
                    self.ref_dict[f"{tr.stored_value_key} #{self.ref_counter}"] = receive['data_dict']
                    self.ref_counter += 1
                if tr.conditional_key != "":
                    self.dictionary[tr.conditional_key] = receive['data_dict']
            else:
                receive = actions(driver, tr, self.logs, None)
                if tr.stored_value_key != "":
                    self.data_dict[tr.stored_value_key] = receive['data']
                    self.ref_dict[f"{tr.stored_value_key} #{self.ref_counter}"] = receive['data']
                    self.ref_counter += 1
                if tr.conditional_key != "":
                    self.dictionary[tr.conditional_key] = receive['data']
                self.logs.log.info(f"For {row}: {vars(tr)}")

            row += 1

    def loop_cases_element(self, driver, row, tr):
        data_dict_loop = {}
        data_dict_element = {}
        data_dict_element_counter = 0
        temp_row = row + 1
        DEMO_END_VALUE = 4
        DEMO_COUNTER = 0
        if tr.stored_value_key != "":
            loop_start_key = tr.stored_value_key
        else:
            loop_start_key = tr.description

        driver.find_element(By.CSS_SELECTOR, tr.locator)  # Adjust based on your locator
        element_list = driver.find_elements(By.CSS_SELECTOR, tr.locator)

        for element in element_list:
            temp_row = row + 1
            tr = TestRow(self.xlwb, temp_row)

            while "end loop" not in tr.description:
                self.logs.log.info(f"LCE loop row: {temp_row}")

                conditional_flag = False
                if tr.conditional_statement != "":
                    receive = self.conditional_module(tr, self.dictionary, self.logs)
                    if receive['conditional_flag']:
                        conditional_flag = True

                if not conditional_flag and tr.conditional_statement != "":
                    self.logs.log.info(f"Condition False for: {vars(tr)}")
                elif "master url" in tr.action:
                    self.master_url = driver.current_url
                    self.master_row = temp_row
                    self.logs.log.info(f"Master url and row allotted: {self.master_row}, {self.master_url}")

                elif "fresh browser" in tr.action:
                    driver.quit()
                    driver = webdriver.Chrome(service=ChromeService(executable_path='/path/to/chromedriver'))
                    driver.get(self.master_url)

                elif tr.action == "create html":
                    create_links_html(self.ref_dict, tr.value, tr.filepath, self.logs)

                elif "start loop" in tr.description:
                    self.logs.log.info(f"Start Loop Module(loop_cases_element): Entry Point #5 {vars(tr)}, {temp_row}")
                    receive = self.start_loop_module(driver, tr, temp_row)
                    self.logs.log.info(f"Start Loop Module(loop_cases_element): Exit Point #5")
                    temp_row = receive['row']

                elif tr.execute != "":
                    receive = self.execute_module(driver, tr, 0)
                    if tr.stored_value_key != "":
                        if receive['data_dict'] != {}:
                            data_dict_element[tr.stored_value_key] = receive['data_dict']
                        self.ref_dict[f"{tr.stored_value_key} #{self.ref_counter}"] = receive['data_dict']
                        self.ref_counter += 1
                    if tr.conditional_key != "":
                        self.dictionary[tr.conditional_key] = receive['data_dict']
                    # --- UPDATE DICTIONARY (for each element) ---
                else:
                    receive = actions(driver, tr, self.logs, element)
                    page = receive['page']

                    # *** STORE IN DICTIONARY (for each action) ***
                    if tr.stored_value_key != "":
                        key = f"{tr.stored_value_key}"
                        data_dict_element[key] = receive['data']
                        self.ref_dict[f"{tr.stored_value_key} #{self.ref_counter}"] = receive['data']
                        self.ref_counter += 1
                    if tr.conditional_key != "":
                        self.dictionary[tr.conditional_key] = receive['data']
                    # --- STORE IN DICTIONARY (for each action) ---

                    self.logs.log.info(
                        f"For {temp_row}: Wait({receive['wait flag']}), Assert({receive['assert flag']}), Action({receive['action flag']}) data:{vars(tr)}")
                    print(
                        f"For {temp_row}: Wait({receive['wait flag']}), Assert({receive['assert flag']}), Action({receive['action flag']}) {vars(tr)}")

                temp_row += 1
                tr = TestRow(self.xlwb, temp_row)
            # --- WHILE LOOP --- end loop command is encountered

            # *** STORE IN DICTIONARY (lce loop dictionary) ***
            data_dict_element_counter += 1
            data_dict_loop[f"{loop_start_key} #{data_dict_element_counter}"] = data_dict_element
            self.ref_dict_loop[self.ref_dict_loop_counter] = data_dict_element
            self.ref_dict_loop_counter += 1
            data_dict_element = {}  # clear element loop for the next element
            # --- STORE IN DICTIONARY (lce loop dictionary) ---

            # *** ASSERTION *** for ending loop prematurely
            if tr.assertion != "" and "continuous" not in tr.description.lower():
                receive = dictionaries(driver, tr.locator, tr.nth, tr.value, tr.assert_value)
                assert_dict = receive['assert_dict']
                receive = execute_assert_code(driver, tr, assert_dict[tr.condition], self.logs)
                if not receive['pass']:
                    break
            # --- ASSERTION ---

            # *** DEMO COUNTER *** ends element loop prematurely
            DEMO_COUNTER += 1
            if DEMO_COUNTER >= DEMO_END_VALUE:
                break
            # --- DEMO COUNTER ---

        # #### finally
        row = temp_row
        send = {'row': row, "data_dict": data_dict_loop}
        return send

    # --- LOOP CASES ELEMENT ---

    def start_loop_module(self, driver, tr, row):
        data_dict_start = {}
        temp_row = row
        continuous_loop_counter = 1
        data_dict_cont = {}
        continuous_flag = True

        while continuous_flag:
            self.logs.log.info(f"SLM loop row: {temp_row}")
            self.logs.log.info(f"Loop Cases Element(slm): Entry Point #6 {temp_row},{tr.locator}, {vars(tr)}")
            temp_row = row
            data = self.loop_cases_element(driver, temp_row, tr)
            self.logs.log.info(f"Loop Cases Element(slm): Exit Point #6")
            temp_row = data['row']

            end_tr = TestRow(self.xlwb, temp_row)
            if end_tr.assertion != "" and "continuous" in end_tr.description:
                receive = dictionaries(driver, end_tr.locator, end_tr.nth, end_tr.value, end_tr.assert_value)
                assert_dict = receive['assert_dict']
                receive = execute_assert_code(driver, end_tr, assert_dict[end_tr.condition], self.logs)
                if not receive['pass']:
                    continuous_flag = False
                    data_dict_start = data_dict_cont
                else:
                    if tr.stored_value_key != "":
                        data_dict_cont[f"{tr.stored_value_key} C#{continuous_loop_counter}"] = data['data_dict']
                    else:
                        data_dict_cont[f"Continuous loop C#{continuous_loop_counter}"] = data['data_dict']
                    continuous_loop_counter += 1
            else:
                data_dict_start = data['data_dict']
                break

        row = temp_row
        send = {'page': driver, 'row': row, 'data_dict': data_dict_start}
        return send

    def execute_module(self, driver, tr: TestRow, counter):
        # Execute two modules depending on data extraction
        self.logs.log.info(f"(ExcelControl/execute_module): {vars(tr)}, {counter}")
        data_dict_execute = {}
        exec_str = tr.execute
        print(exec_str)

        if tr.stored_value_key != "":
            receive = execute_code_get_data(driver, tr, self.logs)
            data_dict_execute[f"{tr.stored_value_key} {counter}"] = receive['data']
        else:
            execute_code(driver, tr, exec_str, self.logs)

        return {'page': driver, 'data_dict': data_dict_execute}

    def conditional_module(self, tr: TestRow, dictionary, logs: Logs):
        # Get the Boolean value of the conditional statement and return it
        self.logs.log.info(f"(ExcelControl/conditional_module): {tr.conditional_statement}")
        conditional_statement = tr.conditional_statement
        conditional_flag = False

        try:
            exec(f"if {conditional_statement}:\n\traise ValueError('Condition is not met')")
            conditional_flag = False
        except Exception:
            conditional_flag = True
        except KeyError:
            print(f"Key {tr.conditional_key} not in dictionary")
            self.logs.log.info(f"Key {tr.conditional_key} not in dictionary")

        print(f"{tr.conditional_statement}: {conditional_flag}")
        return {'conditional_flag': conditional_flag}
