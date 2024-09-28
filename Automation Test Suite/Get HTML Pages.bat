@echo off

:: Define the path to the HTML Pages folder
set "html_pages_folder=%~dp0..\HTML Pages"

:: Check if the HTML Pages folder exists
if not exist "%html_pages_folder%" (
    echo The 'HTML Pages' folder does not exist in the current directory.
    pause
    exit /b
)

:: Open the HTML Pages folder in File Explorer
start "" "%html_pages_folder%"

:: End the script
exit
