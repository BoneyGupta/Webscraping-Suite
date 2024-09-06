from entity.ExcelData import TestRow
from service.Logger import Logs


def row_run_conditional(tr: TestRow, dictionary: dict, dictionary_key, logs: Logs):
    b: bool = True
    if tr.conditional_statement != "":
        logs.log.info("Analysing conditional statement")
        b: bool = True
        exec(f"b = {tr.conditional_statement}")
    send = {'pass': b}
    return send