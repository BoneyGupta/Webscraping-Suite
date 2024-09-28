@echo off
setlocal enabledelayedexpansion

:: Step 1: Ask the user for the name of the new Test file
set /p new_filename="Enter the new name for the Test file (without extension): "

:: Define the paths
set "source_file=..\excel\Test.xlsx"
set "destination_folder=..\excel archives"
set "destination_file=%destination_folder%\%new_filename%.xlsx"

:: Check if the source file exists
if not exist "%source_file%" (
    echo The file 'Test.xlsx' does not exist in the 'excel' folder.
    pause
    exit /b
)

:: Check if the destination folder exists, if not, create it
if not exist "%destination_folder%" (
    echo The 'saved' folder does not exist, creating it...
    mkdir "%destination_folder%"
)

:: Step 2: Move and rename the file
move "%source_file%" "%destination_file%"

:: Check if the move command was successful
if %errorlevel% neq 0 (
    echo Failed to move and rename the file.
    pause
    exit /b
)

echo File moved and renamed to '%new_filename%.xlsx' successfully.
pause
