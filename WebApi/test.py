import os
import shutil
import subprocess
import time
import tkinter
from tkinter import *
from tkinter import ttk, filedialog  # For separator
import webbrowser

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(f"path root dir is {root_dir}")

# Paths for your files
excel_folder_file_path = os.path.join(root_dir, "excel")
excel_archives_path = os.path.join(root_dir, "excel archives")
reports_directory_path = os.path.join(root_dir, "Reports")
html_pages_path = os.path.join(root_dir, "HTML Pages")
run_ats_bat_file_path = os.path.join(root_dir, "Automation Test Suite", "Run-ATS.bat")
api_server_start_bat_file_path = os.path.join(root_dir, "Automation Test Suite", "API-Server-Start.bat")
create_new_chrome_for_logged_sessions_bat_file_path = os.path.join(root_dir, "Automation Test Suite",
                                                                   "Create-New-Chrome-for-Logged-Sessions.bat")
open_logged_in_chrome_bat_file_path = os.path.join(root_dir, "Automation Test Suite", "Open-Logged-in-Chrome.bat")
api_url = "http://127.0.0.1:8001"


def copy_file_to_new_folder(source_file_path, destination_folder, new_filename="Test.xlsx"):
    try:
        shutil.copy(source_file_path, os.path.join(destination_folder, new_filename))
        print(f"File copied successfully to {destination_folder}\\{new_filename}")
    except Exception as e:
        print(f"Error copying file: {e}")


# Function to run a bat file
def run_bat_file(bat_file_path):
    try:
        subprocess.run(bat_file_path, shell=True, check=True)
        print(f"BAT file executed successfully: {bat_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing BAT file: {e}")


# Functions
def open_folder(folder_path):
    if os.path.exists(folder_path):
        os.startfile(folder_path)  # For Windows
    else:
        print("Folder not found!")


def get_latest_report_folder(directory):
    # Find the latest modified directory in the reports folder
    all_sub_dirs = [
        os.path.join(directory, d) for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d))
    ]
    latest_subdir = max(all_sub_dirs, key=os.path.getmtime, default=None)
    return latest_subdir


def open_link(url):
    webbrowser.open_new(url)


def api_server_start():
    run_bat_file(api_server_start_bat_file_path)


def refresh_app():
    # Clear labels or reset any state here if needed
    excel_archives_response_label.config(text="[Response]")  # Resetting the response label


def open_excel_archives():
    open_folder(excel_archives_path)
    excel_archives_response_label.config(text="Process Completed")


def upload_excel_file():
    # Open file dialog to select an .xlsx file
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:  # Check if a file was selected
        destination_folder = excel_archives_path  # Define your destination folder
        destination2_folder = excel_folder_file_path
        new_filename = os.path.basename(file_path)  # Get the name of the selected file
        print(file_path)
        print(destination_folder)
        print(destination2_folder)
        copy_file_to_new_folder(file_path, destination_folder, new_filename)
        copy_file_to_new_folder(file_path, destination2_folder, "Test.xlsx")
        upload_excel_response_label.config(text="Process Completed")


def run_and_download_report():
    run_bat_file(run_ats_bat_file_path)
    time.sleep(5)
    latest_report_folder = get_latest_report_folder(reports_directory_path)
    run_and_download_report_response_label.config(text="Click here for report", fg="blue", cursor="hand2")
    run_and_download_report_response_label.bind("<Button-1>", lambda e: open_folder(latest_report_folder))


def latest_report_folder_link():
    latest_report_folder = get_latest_report_folder(reports_directory_path)
    open_folder(latest_report_folder)


def open_all_reports():
    open_folder(reports_directory_path)
    all_reports_response_label.config(text="Process Complete")


def create_new_chrome_for_logged_session():
    run_bat_file(create_new_chrome_for_logged_sessions_bat_file_path)


def open_logged_in_chrome():
    run_bat_file(open_logged_in_chrome_bat_file_path)


# Create main window
root = Tk()
root.geometry("800x800")
root.title("Button Function with Links and Layout")

# Set window icon (title bar)
root.iconbitmap("app_icon.ico")  # Ensure this file is in the same directory

# Set taskbar icon (ensure the file exists)
taskbar_icon = PhotoImage(file="app_icon.png")
root.iconphoto(True, taskbar_icon)

# API Server Start
api_server_start_button = Button(root, text="Start API Server and Open Swagger Docs", command=api_server_start)
api_server_start_button.grid(row=0, column=0, columnspan=3, pady=5, sticky="w")

# Refresh button
refresh_button = Button(root, text="Refresh", command=refresh_app)
refresh_button.grid(row=0, column=2, columnspan=3, pady=5, sticky="se")

# Excel Archives
excel_archives_heading = Label(root, text="Excel Archives", font=("Arial", 14))
excel_archives_heading.grid(row=1, column=0, columnspan=3, pady=5, sticky="w")
excel_archives_desc = Label(root, text="Open the folder to view all the excel workbooks created.")
excel_archives_desc.grid(row=2, column=0, columnspan=3, sticky="w")
open_excel_archives_button = Button(root, text="Open Folder", command=open_excel_archives)
open_excel_archives_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")
excel_archives_response_label = Label(root, text="[Response]")
excel_archives_response_label.grid(row=3, column=1, sticky="w")
download_excel_archives_api_link = Label(root, text="Test API : Download Excel archives", fg="blue", cursor="hand2")
download_excel_archives_api_link.bind("<Button-1>", lambda e: open_link(api_url + "/download-excel-archives"))
download_excel_archives_api_link.grid(row=3, column=2, sticky="w")
excel_archives_sub_text = Label(root,
                                text="Refer or make changes to these workbooks and save the workbook in the Excel folder as test.xlsx to run the test.",
                                font=("Arial", 8), fg="gray")
excel_archives_sub_text.grid(row=4, column=0, columnspan=3, sticky="w", padx=0, pady=5)
open_excel_archives_link = Label(root, text="Open Excel Archives", fg="blue", cursor="hand2")
open_excel_archives_link.grid(row=4, column=3, sticky="w", padx=0, pady=5)
open_excel_archives_link.bind("Link-Open-Excel-Archives", lambda e: open_folder(excel_archives_path))
separator1 = ttk.Separator(root, orient="horizontal")
separator1.grid(row=5, column=0, columnspan=4, sticky="ew", pady=10)

# Upload Excel Workbook
upload_excel_heading = Label(root, text="Upload Excel WorkBook", font=("Arial", 14))
upload_excel_heading.grid(row=6, column=0, columnspan=3, pady=5, sticky="w")
upload_excel_desc = Label(root, text="Upload Excel for testing and save it to archives as well.")
upload_excel_desc.grid(row=7, column=0, columnspan=3, sticky="w")
upload_excel_button = Button(root, text="Upload .xlsx File", command=upload_excel_file)
upload_excel_button.grid(row=8, column=0, padx=10, pady=5, sticky="w")
upload_excel_response_label = Label(root, text="[Response]")
upload_excel_response_label.grid(row=8, column=1, sticky="w")
upload_excel_api_link = Label(root, text="Test API : Upload Excel Files", fg="blue", cursor="hand2")
upload_excel_api_link.bind("<Button-1>", lambda e: open_link(api_url + "/upload-test-xlsx"))
upload_excel_api_link.grid(row=8, column=2, sticky="w")
upload_excel_sub_text = Label(root,
                              text="This file will be processed at program run. You can view your document at Excel Archives.",
                              font=("Arial", 8), fg="gray")
upload_excel_sub_text.grid(row=9, column=0, columnspan=3, sticky="w", padx=0, pady=5)
upload_excel_archives_link = Label(root, text="Open Current Test Folder", fg="blue", cursor="hand2")
upload_excel_archives_link.grid(row=9, column=3, sticky="w", padx=0, pady=5)
upload_excel_archives_link.bind("<Button-1>", lambda e: open_folder(excel_folder_file_path))
separator1 = ttk.Separator(root, orient="horizontal")
separator1.grid(row=10, column=0, columnspan=4, sticky="ew", pady=10)

# Run ATS and Download Report
run_and_download_report_heading = Label(root, text="Run and Open Reports", font=("Arial", 14))
run_and_download_report_heading.grid(row=11, column=0, columnspan=3, pady=5, sticky="w")
run_and_download_report_desc = Label(root,
                                     text="Runs Test.xlsx/Latest Uploaded Document and opens the report folder .")
run_and_download_report_desc.grid(row=12, column=0, columnspan=3, sticky="w")
run_and_download_report_button = Button(root, text="Run", command=run_and_download_report)
run_and_download_report_button.grid(row=13, column=0, padx=10, pady=5, sticky="w")
run_and_download_report_response_label = Label(root, text="[Response]")
run_and_download_report_response_label.grid(row=13, column=1, sticky="w")
run_and_download_report_api_link = Label(root, text="Test API : Run ATS and Download Reports", fg="blue",
                                         cursor="hand2")
run_and_download_report_api_link.bind("<Button-1>", lambda e: open_link(api_url + "/run-ats-and-download-report"))
run_and_download_report_api_link.grid(row=13, column=2, sticky="w")
run_and_download_report_link0 = Label(root, text="Addtitional Links    ---->", fg="black")
run_and_download_report_link0.grid(row=14, column=0, sticky="w", padx=0, pady=5)
run_and_download_report_link1 = Label(root, text="Open Latest Report Folder", fg="blue", cursor="hand2")
run_and_download_report_link1.grid(row=14, column=1, sticky="w", padx=0, pady=5)
run_and_download_report_link1.bind("<Button-1>", lambda e: latest_report_folder_link())
run_and_download_report_link2 = Label(root, text="Open HTML Pages Folder", fg="blue", cursor="hand2")
run_and_download_report_link2.grid(row=14, column=2, sticky="w", padx=0, pady=5)
run_and_download_report_link2.bind("<Button-1>", lambda e: open_folder(html_pages_path))
run_and_download_report_link3 = Label(root, text="Open Current Test Folder", fg="blue", cursor="hand2")
run_and_download_report_link3.grid(row=14, column=3, sticky="w", padx=0, pady=5)
run_and_download_report_link3.bind("<Button-1>", lambda e: open_folder(excel_folder_file_path))
separator1 = ttk.Separator(root, orient="horizontal")
separator1.grid(row=15, column=0, columnspan=4, sticky="ew", pady=10)

# All Reports
all_reports_heading = Label(root, text="All Reports", font=("Arial", 14))
all_reports_heading.grid(row=16, column=0, columnspan=3, pady=5, sticky="w")
all_reports_desc = Label(root, text="Opens the reports folder with all reports.")
all_reports_desc.grid(row=17, column=0, columnspan=3, sticky="w")
all_reports_button = Button(root, text="Open folder", command=open_all_reports)
all_reports_button.grid(row=18, column=0, padx=10, pady=5, sticky="w")
all_reports_response_label = Label(root, text="[Response]")
all_reports_response_label.grid(row=18, column=1, sticky="w")
all_reports_api_link = Label(root, text="Test API : Download Reports Folder", fg="blue", cursor="hand2")
all_reports_api_link.bind("<Button-1>", lambda e: open_link(api_url + "/download-all-reports"))
all_reports_api_link.grid(row=18, column=2, sticky="w")
all_reports_link = Label(root, text="Open Reports Folder", fg="blue", cursor="hand2")
all_reports_link.grid(row=19, column=3, sticky="w", padx=0, pady=5)
all_reports_link.bind("<Button-1>", lambda e: open_folder(reports_directory_path))
separator1 = ttk.Separator(root, orient="horizontal")
separator1.grid(row=20, column=0, columnspan=4, sticky="ew", pady=10)

# Logged in Chrome
logged_in_chrome_heading = Label(root, text="Logged in Chrome", font=("Arial", 14))
logged_in_chrome_heading.grid(row=21, column=0, columnspan=3, pady=5, sticky="w")
logged_in_chrome_desc = Label(root,
                              text="Create for the first time or Open Logged in Chrome sessions to by pass complex logins/captcha.")
logged_in_chrome_desc.grid(row=22, column=0, columnspan=3, sticky="w")
create_logged_in_chrome_button = Button(root, text="Create(First Time Only)",
                                        command=create_new_chrome_for_logged_session)
create_logged_in_chrome_button.grid(row=23, column=0, padx=10, pady=5, sticky="w")
create_logged_in_chrome_api_link = Label(root, text="Test API : Create New Chrome for Logged Sessions", fg="blue",
                                         cursor="hand2")
create_logged_in_chrome_api_link.bind("<Button-1>",
                                      lambda e: open_link(api_url + "/create-new-chrome-for-logged-sessions"))
create_logged_in_chrome_api_link.grid(row=23, column=2, sticky="w")
open_logged_in_chrome_button = Button(root, text="Open Logged in Chrome",
                                      command=create_new_chrome_for_logged_session)
open_logged_in_chrome_button.grid(row=24, column=0, padx=10, pady=5, sticky="w")
open_logged_in_chrome_api_link = Label(root, text="Test API : Open Logged in Chrome", fg="blue",
                                       cursor="hand2")
open_logged_in_chrome_api_link.bind("<Button-1>", lambda e: open_link(api_url + "/open-logged-in-chrome"))
open_logged_in_chrome_api_link.grid(row=24, column=2, sticky="w")
separator1 = ttk.Separator(root, orient="horizontal")
separator1.grid(row=25, column=0, columnspan=4, sticky="ew", pady=10)

# Start the Tkinter event loop
root.mainloop()
