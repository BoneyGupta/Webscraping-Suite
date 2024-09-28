@echo off
setlocal

:: Step 1: Define the path to Test.xlsx
set "file_path=%~dp0..\excel\Test.xlsx"

:: Step 2: Check if Test.xlsx exists
if exist "%file_path%" (
    echo Test.xlsx found. Opening the file...
    start "" "%file_path%"
) else (
    echo Test.xlsx does not exist in the current directory. Create a New Test
)

exit
