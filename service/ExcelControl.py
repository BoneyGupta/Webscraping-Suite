import threading
import time
import traceback

from playwright.sync_api import expect

from entity.ExcelData import ExcelWorkBook, TestRow
from service.ActionFunctions import execute_code_get_data, execute_code
from service.AssertCodes import execute_assert_code
from service.Browser import *
from service.CodeCreate import actions, dictionaries
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

    def __init__(self, pw: Playwright, xlwb: ExcelWorkBook, logs: Logs):
        self.pw = pw
        self.xlwb = xlwb
        self.logs = logs

    def config(self):
        """
        Driver class for the Excel workbook test cases.
        Can only work with one excel workbook
        :return:
        """
        # Change Sheet to Test Details
        self.xlwb.change_sheet(self.xlwb.sheet_names.index("Details"))

        # Create Object for test Details
        td = TestDetails(self.xlwb)

        print(f"WorkBook Sheets: {self.xlwb.sheet_names}  ({self.xlwb.sheet_count})")

        # Run an already logged in browser if cdp is True
        if td.cdp:
            t = threading.Thread(target=open_browser_in_debugging_mode)
            t.start()
            t.join(timeout=5)
            os.chdir('..')
            time.sleep(5)

        # Create Playwright objects for browser, browser-context and page
        browser = select_browser(self.pw, td.browser, td.headless, td.cdp)
        context = open_browser_context(browser, td.cdp)
        page = open_page(context, td.cdp)

        url = td.website
        page.goto(url)  # Opens the website

        # Iterates through the sheets and checks if the sheet name has test in it
        for i in range(0, self.xlwb.sheet_count):
            self.logs.log.info(f"Sheet loop number: {i}")
            if "test" in self.xlwb.sheet_names[i].lower():
                self.xlwb.change_sheet(i)
                # while True:
                try:
                    self.logs.log.info(f"** sheets: Entry Point #2 ** {self.xlwb.sheet_names[i]}")
                    self.sheets(page, self.xlwb.sheet_names[i])
                    self.logs.log.info(f"** sheets: Exit Point #2 **")
                    # break
                except Exception as e:
                    screenshot_file = f"{self.logs.directory_path}/screenshot-config-{time.strftime('%Y-%m-%d %H%M%S')}.png"
                    self.logs.log.critical(f"Sheet: {self.xlwb.sheet_names[i]}\n Screenshot: {screenshot_file}")
                    page.screenshot(path=screenshot_file, timeout=100000)
                    self.logs.log.error(f"{self.xlwb.sheet_names[i]} did not process complete. Continue with next test")
                    print(f"Error: {str(e)}")
                    self.logs.log.info(f"Error: {str(e)}")
                    raise
                    # if self.master_url != "":
                    #     self.logs.log.warning(f"{self.xlwb.sheet_names[i]}: Retrying using master url")
                    #     receive = fresh_browser(self.pw, True, self.master_url)
                    #     page = receive['page']
                    # else:
                    #     self.logs.log.error(f"{self.xlwb.sheet_names[i]} did not process complete. Continue with next test")
                    #     break
                finally:
                    print(f"Data Dictionary: {self.data_dict}")
                    print(f"Reference Dictionary: {self.ref_dict}")
                    print(f"Loop Reference Dictionary: {self.ref_dict_loop}")
                    # if not td.cdp:
                    JsonHandler.create_json_file(f"{self.logs.directory_path}/data{time.strftime('%H%M%S')}.json",
                                                 self.data_dict)
                    JsonHandler.create_json_file(
                        f"{self.logs.directory_path}/reference_data{time.strftime('%H%M%S')}.json", self.ref_dict)
                    JsonHandler.create_json_file(
                        f"{self.logs.directory_path}/ref_loop_data{time.strftime('%H%M%S')}.json", self.ref_dict_loop)
                    # else:
                    #     self.logs.data.info(self.data_dict)
                    #     self.logs.ref_data.info(self.ref_dict)
                    #     self.logs.ref_data.info(self.ref_dict_loop)

        # time.sleep(15)
        close_page(page)
        close_browser_context(context)
        close_browser(browser)

    def sheets(self, page: Page, sheet_name: str):

        print("Current testing: " + sheet_name)

        # *** INITIALIZE ***
        global receive
        exec_str: str
        # --- INITIALIZE ---

        row = 3
        while row <= self.xlwb.get_rows_count():
            # #### traversing through each row one by one and creating objects for each row
            self.logs.log.info(f"Sheet row: {row}")

            tr = TestRow(self.xlwb, row)  # get row object.

            # *** Conditional Statement ***
            conditional_flag = False
            if tr.conditional_statement != "":
                receive = self.conditional_module(tr, self.dictionary, self.logs)
                if not receive['conditional_flag']:
                    conditional_flag = True
            # --- Conditional Statement ---

            if not conditional_flag and tr.conditional_statement != "":
                self.logs.log.info(f"Condition False for: {tr}")

            elif "master url" in tr.action:
                # #### saves master url and row to continue execution if test fails
                self.master_url = page.url
                self.master_row = row
                self.logs.log.info(f"Master url and row allotted: {self.master_row}, {self.master_url}")

            elif "fresh browser" in tr.action:
                # #### closes browser and opens a new one
                receive = fresh_browser(self.pw, page, True, self.master_url)
                page = receive['page']
                temp_row = self.master_row - 1

            elif tr.action == "create html":
                # #### creates html links from the links received in ref_dict_loop
                create_links_html(self.ref_dict, tr.value, tr.filepath, self.logs)

            elif "start loop" in tr.description:

                # *** START LOOP MODULE ***
                self.logs.log.info(f"Start Loop Module(sheets): Entry Point #3 {vars(tr)},{row}")
                receive = self.start_loop_module(page, tr, row)
                self.logs.log.info(f"Start Loop Module(sheets): Exit Point #3")
                page = receive['page']
                row = receive['row']
                # --- START LOOP MODULE ---

                # *** STORE IN DICTIONARY (sheet loop dictionary) ---
                if tr.stored_value_key != "":
                    self.data_dict[tr.stored_value_key] = receive['data_dict']
                else:
                    self.data_dict[tr.description] = receive['data_dict']
                # --- STORE IN DICTIONARY (sheet loop dictionary) ---

            elif tr.execute != "":
                # #### runs code with exec()
                receive = self.execute_module(page, tr, "")

                # *** UPDATE DICTIONARY (for each execute) ***
                if tr.stored_value_key != "":
                    if receive['data_dict'] != {}:
                        self.data_dict[tr.stored_value_key] = receive['data_dict']
                    self.ref_dict[f"{tr.stored_value_key} #{self.ref_counter}"] = receive['data_dict']
                    self.ref_counter += 1
                if tr.conditional_key != "":
                    self.dictionary[tr.conditional_key] = receive['data_dict']
                # --- UPDATE DICTIONARY (for each execute) ---
            else:
                receive = actions(self.pw, page, tr, self.logs, None)
                page = receive['page']

                # *** STORE IN DICTIONARY (for each action) ***
                if tr.stored_value_key != "":
                    self.data_dict[tr.stored_value_key] = receive['data']
                    self.ref_dict[f"{tr.stored_value_key} #{self.ref_counter}"] = receive['data']
                    self.ref_counter += 1
                if tr.conditional_key != "":
                    self.dictionary[tr.conditional_key] = receive['data']
                # --- STORE IN DICTIONARY (for each action) ---
                self.logs.log.info(
                    f"For {row}: Wait({receive['wait flag']}), Assert({receive['assert flag']}), Action({receive['action flag']}) data:{vars(tr)}")
                print(
                    f"For {row}: Wait({receive['wait flag']}), Assert({receive['assert flag']}), Action({receive['action flag']}) {vars(tr)}")
            row += 1
            # --- WHILE LOOP --- end loop command is encountered

    # --- SHEETS ---

    def loop_cases_element(self, page: Page, row: int, tr: TestRow):

        # *** INITIALIZATION ***
        data_dict_loop: dict = {}  # Module dictionary
        data_dict_element: dict = {}  # Element loop dictionary
        data_dict_element_counter = 0  # Element loop dictionary key name
        temp_row = row + 1  # The row after the row where start loop command is given
        DEMO_END_VALUE = 4
        DEMO_COUNTER = 0
        if tr.stored_value_key != "":
            loop_start_key = tr.stored_value_key  # Module dictionary key name
        else:
            loop_start_key = tr.description  # Module dictionary key name
        # ---INITIALIZATION ---

        # *** ELEMENT LIST *** extract element list from the locator in start loop row
        try:
            receive = actions(self.pw, page, tr, self.logs, None)
        except Exception as e:
            page.screenshot(path=f"{self.logs.directory_path}/screenshot-lce-{time.strftime('%Y-%m-%d %H%M%S')}.png",
                            timeout=100000)
            raise
        self.logs.code_prog.info(f"element_list: list = page.locator({tr.locator}).all()")
        element_list: list = page.locator(tr.locator).all()
        # --- ELEMENT LIST ---

        for element in element_list:
            # #### for each element corresponding to the loop locator

            temp_row = row + 1  # Reinitialize temp_row every time loop runs for next element
            tr = TestRow(self.xlwb, temp_row)  # Row Object for each row

            # *** WHILE LOOP *** loop runs next row till it encounters 'end loop'
            while "end loop" not in tr.description:
                # #### ends when encountering 'end loop'
                print(f"Working with: {vars(tr)}")

                self.logs.log.info(f"LCE loop row: {temp_row}")

                # *** Conditional Statement ***
                conditional_flag = False
                if tr.conditional_statement != "":
                    receive = self.conditional_module(tr, self.dictionary, self.logs)
                    if receive['conditional_flag']:
                        conditional_flag = True
                # --- Conditional Statement ---

                if not conditional_flag and tr.conditional_statement != "":
                    self.logs.log.info(f"Condition False for: {vars(tr)}")
                elif "master url" in tr.action:
                    # #### saves master url and row to continue execution if test fails
                    self.master_url = page.url
                    self.master_row = temp_row
                    self.logs.log.info(f"Master url and row allotted: {self.master_row}, {self.master_url}")

                elif "fresh browser" in tr.action:
                    # #### closes browser and opens a new one
                    receive = fresh_browser(self.pw, page, True, self.master_url)
                    page = receive['page']
                    temp_row = self.master_row - 1

                elif tr.action == "create html":
                    # #### creates html links from the links received in ref_dict_loop
                    create_links_html(self.ref_dict, tr.value, tr.filepath, self.logs)

                elif "start loop" in tr.description:
                    # *** START LOOP MODULE ***
                    self.logs.log.info(f"Start Loop Module(loop_cases_element) : Entry Point #5 {vars(tr)}, {temp_row}")
                    receive = self.start_loop_module(page, tr, temp_row)
                    self.logs.log.info(f"Start Loop Module(loop_cases_element) : Exit Point #5")
                    temp_row = receive['row']  # Gets the end loop row for the loop
                    # --- START LOOP MODULE ---

                    # *** UPDATE DICTIONARY (for each element) *** element loop
                    data_dict_element.update(receive['data_dict'])
                    # --- UPDATE DICTIONARY (for each element) ---

                elif tr.execute != "":
                    # #### runs code with exec()
                    receive = self.execute_module(page, tr, 0)

                    # *** UPDATE DICTIONARY (for each element) *** element loop, reference dictionary
                    if tr.stored_value_key != "":
                        if receive['data_dict'] != {}:
                            data_dict_element[tr.stored_value_key] = receive['data_dict']
                        self.ref_dict[f"{tr.stored_value_key} #{self.ref_counter}"] = receive['data_dict']
                        self.ref_counter += 1
                    if tr.conditional_key != "":
                        self.dictionary[tr.conditional_key] = receive['data_dict']
                    # --- UPDATE DICTIONARY (for each element) ---
                else:
                    receive = actions(self.pw, page, tr, self.logs, element)
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
                receive = dictionaries(page, tr.locator, tr.nth, tr.value, tr.assert_value)
                assert_dict = receive['assert_dict']
                receive = execute_assert_code(self.pw, page, tr, assert_dict[tr.condition], self.logs)
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

    def start_loop_module(self, page: Page, tr: TestRow, row: int) -> dict:
        """

        """
        # *** INITIALIZATION ***
        data_dict_start: dict = {}
        temp_row = row  # Row where 'start loop' command is given
        continuous_loop_counter = 1  # For continuous loop key name
        data_dict_cont: dict = {}  # Dictionary for 'end loop' 'continuous'
        continuous_flag = True
        DEMO_COUNTER_CONTINUOUS = 0  # Only for demo. Comment it otherwise
        DEMO_END_VALUE_CONTINUOUS = 3
        DEMO_CONTINUOUS_FLAG = True
        # --- INITIALIZATION ---

        while continuous_flag:
            # #### to persist the loop till 'Assertion' becomes 'False'

            if DEMO_CONTINUOUS_FLAG:
                # *** DEMO COUNTER *** end continuous loop prematurely
                if DEMO_COUNTER_CONTINUOUS >= DEMO_END_VALUE_CONTINUOUS:
                    data_dict_start = data_dict_cont
                    continuous_flag = False
                    # ### finally
                    row = temp_row
                    send = {'page': page, 'row': row, 'data_dict': data_dict_start}
                    return send
                # --- DEMO COUNTER --- break after storing data in loop dictionary

            # *** LOOP CASES ELEMENT ***
            self.logs.log.info(f"SLM loop row: {temp_row}")
            self.logs.log.info(f"Loop Cases Element(slm): Entry Point #6 {temp_row},{tr.locator}, {vars(tr)}")
            temp_row = row
            data = self.loop_cases_element(page, temp_row, tr)
            self.logs.log.info(f"Loop Cases Element(slm): Exit Point #6")
            temp_row = data['row']  # Update row value to the last row
            # --- LOOP CASES ELEMENT ---

            # *** START: END LOOP CONTINUOUS ***
            end_tr = TestRow(self.xlwb, temp_row)
            if end_tr.assertion != "" and "continuous" in end_tr.description:

                # *** DEMO COUNTER *** end continuous loop prematurely
                if DEMO_COUNTER_CONTINUOUS >= DEMO_END_VALUE_CONTINUOUS:
                    data_dict_start = data_dict_cont
                    continuous_flag = False
                    # ### finally
                    row = temp_row
                    send = {'page': page, 'row': row, 'data_dict': data_dict_start}
                    return send
                DEMO_COUNTER_CONTINUOUS += 1
                # --- DEMO COUNTER --- break after storing data in loop dictionary

                # *** ASSERTION *** start assertion for end loop continuous
                receive = dictionaries(page, end_tr.locator, end_tr.nth, end_tr.value, end_tr.assert_value)
                assert_dict = receive['assert_dict']
                receive = execute_assert_code(self.pw, page, end_tr, assert_dict[end_tr.condition], self.logs)
                # --- ASSERTION --- end assertion for end loop continuous

                # *** STORE IN DICTIONARY (end loop continuous) *** start storage sequence
                if not receive['pass']:
                    # ####'Assert'>> 'False' ends the continuous loop and stores data in  main loop dictionary
                    data_dict_start = data_dict_cont
                    break
                else:
                    # #### 'Assert'>> 'True' stores data in continuous loop dictionary
                    if tr.stored_value_key != "":
                        data_dict_cont[f"{tr.stored_value_key} C#{continuous_loop_counter}"] = data['data_dict']
                    else:
                        data_dict_cont[f"Continuous loop C#{continuous_loop_counter}"] = data['data_dict']
                    continuous_loop_counter += 1
                # --- STORE IN DICTIONARY (end loop continuous) --- end storage sequence in if block
            # --- END LOOP CONTINUOUS ---
            else:
                # ***STORE IN DICTIONARY (start loop module)*** start storage sequence in else block
                data_dict_start = data['data_dict']
                # --- STORE IN DICTIONARY (start loop module) --- end storage sequence in else block
                break
        # #### while true ends here

        # ### finally
        row = temp_row
        send = {'page': page, 'row': row, 'data_dict': data_dict_start}
        return send
        # --- START LOOP MODULE ---

    def execute_module(self, page: Page, tr: TestRow, counter):
        # execute two modules depending of data extraction
        self.logs.log.info(f"(ExcelControl/execute_module): {vars(tr)},{counter}")
        data_dict_execute: dict = {}
        exec_str = tr.execute
        print(exec_str)
        if tr.stored_value_key != "":
            receive = execute_code_get_data(self.pw, page, tr, self.logs)
            data_dict_execute[f"{tr.stored_value_key} {counter}"] = receive['data']
        else:
            execute_code(self.pw, page, tr, exec_str, self.logs)

        send = {'page': page, 'data_dict': data_dict_execute}
        return send

    def conditional_module(self, tr: TestRow, dictionary, logs: Logs):
        # get the Boolean value of the conditional statement and return it
        self.logs.log.info(f"(ExcelControl/conditonal_module): {tr.conditional_statement} ")
        conditional_statement = tr.conditional_statement
        conditional_flag: bool = False
        try:
            exec(f"if {conditional_statement}:\n\traise ValueError(\"Condition is not met\")")
            conditional_flag = False
        except Exception:
            conditional_flag = True
        except KeyError:
            print(f"Key {tr.conditional_key} not in dictionary")
            self.logs.log.info(f"Key {tr.conditional_key} not in dictionary")
        print(f"{tr.conditional_statement}: {conditional_flag}")
        send = {'conditional_flag': conditional_flag}
        return send
