@echo off

:: Define the path to the Reports folder
set "reports_folder=%~dp0..\Reports"

:: Check if the Reports folder exists
if not exist "%reports_folder%" (
    echo The 'Reports' folder does not exist in the current directory.
    pause
    exit /b
)

:: Open the Reports folder in File Explorer
start "" "%reports_folder%"

:: End the script
exit
