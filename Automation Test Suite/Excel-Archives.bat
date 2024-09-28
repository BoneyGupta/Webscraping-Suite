@echo off

:: Define the path to the excel folder
set "excel_folder=%~dp0..\excel archives"

:: Check if the excel folder exists
if not exist "%excel_folder%" (
    echo The 'excel' folder does not exist in the current directory.
    pause
    exit /b
)

:: Open the excel folder in File Explorer
start "" "%excel_folder%"

:: End the script
exit
