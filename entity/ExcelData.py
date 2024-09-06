from entity.Constants import *
from utils.Excel import Excel


class ExcelWorkBook(Excel):
    def __init__(self, file_path: str, sheet_count: None, sheet_names: None, rows: None, columns: None):
        super().__init__(file_path)
        self.sheet_count = super().get_sheet_count()
        self.sheet_names = super().get_sheet_names()

    def get_cell(self, row, col):
        if super().is_cell_empty(row, col):
            return ""
        return super().get_cell_value(row, col)


class TestDetails:
    def __init__(self, xlwb: ExcelWorkBook):
        self.xlwb = xlwb
        self.TEST_DATA_COLUMN = 2
        self.test_name: str = self.xlwb.get_cell(TEST_NAME, self.TEST_DATA_COLUMN)
        self.browser: str = self.xlwb.get_cell(BROWSER, self.TEST_DATA_COLUMN).lower()
        self.website: str = self.xlwb.get_cell(WEBSITE, self.TEST_DATA_COLUMN).lower()
        self.headless: bool = self.xlwb.get_cell(HEADLESS, self.TEST_DATA_COLUMN)
        self.screenshot: str = self.xlwb.get_cell(SCREENSHOT, self.TEST_DATA_COLUMN).lower()
        self.video: str = self.xlwb.get_cell(VIDEO, self.TEST_DATA_COLUMN).lower()
        self.framework: str = self.xlwb.get_cell(FRAMEWORK, self.TEST_DATA_COLUMN).lower()
        self.cdp: bool = self.xlwb.get_cell(CDP, self.TEST_DATA_COLUMN)


class TestRow:
    def __init__(self, xlwb: ExcelWorkBook, row: int):
        self.xlwb = xlwb
        self.element_id: int = self.xlwb.get_cell(row, ELEMENT_ID)
        self.description: str = self.xlwb.get_cell(row, DESCRIPTION)
        self.execute: str = self.xlwb.get_cell(row, EXECUTE)
        self.locator: str = self.xlwb.get_cell(row, LOCATOR)
        self.action: str = self.xlwb.get_cell(row, ACTION).lower()
        self.value = self.xlwb.get_cell(row, VALUE)
        self.assertion: str = self.xlwb.get_cell(row, ASSERT).lower()
        self.condition = self.xlwb.get_cell(row, CONDITION)
        self.stored_value_key: str = self.xlwb.get_cell(row, STORED_VALUE_KEY)
        self.timeout: int = self.xlwb.get_cell(row, WAIT)
        self.url: str = self.xlwb.get_cell(row, URL_ROW)
        self.filepath: str = self.xlwb.get_cell(row, FILEPATH)
        self.assert_value = self.xlwb.get_cell(row, ASSERT_VALUE)
        self.nth = self.xlwb.get_cell(row, NTH)
        self.conditional_key = self.xlwb.get_cell(row, CONDITIONAL_KEY)
        self.conditional_statement = self.xlwb.get_cell(row, CONDITIONAL_STATEMENT)
