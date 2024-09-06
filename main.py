import time

from playwright.sync_api import Playwright, sync_playwright

from entity.ExcelData import TestDetails, ExcelWorkBook
from service.ExcelControl import StartTest

from service.Browser import *
from service.Logger import Logs


def run(self: Playwright) -> None:
    # Open Excel WorkBook and create object
    xlwb = ExcelWorkBook("excel\\Test.xlsx", None, None,
                         None, None)

    # Create Logger object
    logger = Logs()

    logger.log.info(f"StartTest.config: Entry Point #1")
    logger.log.info(f"StartTest.config: {vars(xlwb)}, {vars(logger)}")
    start = StartTest(self, xlwb, logger)
    start.config()
    logger.log.info(f"StartTest.config: Exit Point #1")

    xlwb.close_workbook()


start_time = time.time()

with sync_playwright() as playwright:
    run(playwright)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
