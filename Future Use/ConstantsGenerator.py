from entity.ExcelData import ExcelWorkBook

xl = ExcelWorkBook("../excel/Test.xlsx", None, None, None, None)

details: dict = {}
test_sheet: dict = {}


def generate_constants_details():
    xl.change_sheet(xl.sheet_names.index("Details"))

    details_counter = 0
    for row in range(1, xl.get_rows_count()):
        details_counter += 1
        details[xl.get_cell(row, 1)] = {'row': details_counter, 'data': xl.get_cell(row, 2)}

    print("Details:")
    for key in details:
        print(key, details[key]['row'], details[key]['data'])


def generate_constants_sheet(sheet_name):
    xl.change_sheet(xl.sheet_names.index(sheet_name))

    heading_counter = 0

    col_data = xl.get_cell(1, 1)
    while col_data != "":
        heading_counter += 1
        test_sheet[xl.get_cell(2, heading_counter)] = {'col': heading_counter, 'data': col_data}
        col_data = xl.get_cell(2, heading_counter + 1)

    print("Test Sheet:")
    for key in test_sheet:
        print(key, test_sheet[key]['col'])


generate_constants_details()
generate_constants_sheet('test sheet 1')
