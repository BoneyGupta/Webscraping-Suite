import os
import time

from utils.Logging import Logging


class Logs:
    def __init__(self):

        # Create a runtime directory for reports
        directory = f"Reports"
        try:
            os.mkdir(directory)
            print("Directory created successfully.")
        except FileExistsError:
            print("Directory already exists.")

        # Create a runtime directory for chromedata
        directory = f"chromedata"
        try:
            os.mkdir(directory)
            print("Directory created successfully.")
        except FileExistsError:
            print("Directory already exists.")

            # Create a runtime directory for reports in Reports
        directory = f"Report {time.strftime('%Y-%m-%d %H%M%S')}"
        self.directory_path = f"Reports/{directory}"
        try:
            os.mkdir(self.directory_path)
            print("Directory created successfully.")
        except FileExistsError:
            print("Directory already exists.")

        self.code_prog = Logging(f"{self.directory_path}/code_prog.log", False)
        self.log = Logging(f"{self.directory_path}/logs.log", True)
        # self.data = Logging(f"{self.directory_path}/data.log", False)
        # self.ref_data = Logging(f"{self.directory_path}/reference data.log", False)
        # self.ref_loop_data = Logging(f"{self.directory_path}/reference loop data.log", False)

        self.code_prog.info("Logger initialized")
        self.log.info("Logger initialized")
