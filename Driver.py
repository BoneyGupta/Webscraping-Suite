# import os
#
# from entity.ExcelData import ExcelWorkBook
#
#
# def driver():
#     # Open Excel WorkBook and create object
#     xlwb = ExcelWorkBook("excel\\Driver.xlsx", None, None,
#                          None, None)
#     driver_dict = {}
#
#     for row in range(1, xlwb.get_rows_count() + 1):
#         key = xlwb.get_cell_value(row, 1)
#         value = xlwb.get_cell_value(row, 2)
#         driver_dict[key] = value
#     print(driver_dict)
#
#     shell_code = f"pytest "
#
#     for key in driver_dict:
#         if driver_dict[key] is not None:
#             if key == "m":
#                 shell_code += f"-m {driver_dict[key]} "
#             elif "yes" not in str(driver_dict[key]):
#                 shell_code += f"--{key}={driver_dict[key]} "
#             else:
#                 shell_code += f"--{key} "
#
#     # shell_code += "Logger.py"
#
#     print(shell_code)
#
#     output = os.system(shell_code)
#     print(output)
#
#     # output = sh.Command("your_command_here")()
#     # print(output)
#
#
# driver()
