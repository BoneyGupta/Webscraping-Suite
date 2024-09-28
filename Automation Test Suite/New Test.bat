@echo off
setlocal enabledelayedexpansion

:: Step 1: Define the excel folder path
set "excel_folder=%~dp0..\excel archives"

:: Check if the excel folder exists
if not exist "%excel_folder%" (
    echo The 'excel' folder does not exist in the current directory.
    pause
    exit /b
)

:: Step 1: Display all the .xlsx files in the excel folder
echo Available .xlsx files in the excel folder:
set count=0

for %%f in ("%excel_folder%\*.xlsx") do (
    set /a count+=1
    echo !count!. %%~nxf
    set "file!count!=%%~f"
)

:: If no .xlsx files found, exit
if %count%==0 (
    echo No .xlsx files found in the 'excel' folder.
    pause
    exit /b
)

:: Step 2: Prompt the user to select a file
set /p choice="Enter the number corresponding to the file you want to select: "

:: Check if the user's choice is valid
if not defined file%choice% (
    echo Invalid choice. Exiting.
    pause
    exit /b
)

set "target=..\excel\Test.xlsx"

:: Check if the target file Test.xlsx already exists
if exist "%target%" (
    echo WARNING: Test.xlsx already exists.
    choice /m "Do you want to overwrite it? (Y/N)" /c YN /n
    if errorlevel 2 (
        echo Operation cancelled by the user.
        pause
        exit /b
    )
)

set "selected_file=!file%choice%!"

:: Step 3: Copy the selected file and save it as Test.xlsx
set "test_file=%~dp0..\excel\Test.xlsx"
copy /y "%selected_file%" "%test_file%"

if %errorlevel% neq 0 (
    echo Failed to copy the file.
    pause
    exit /b
)

echo File copied as Test.xlsx.

:: Step 4: Open Test.xlsx
start "" "%test_file%"

echo Task completed.
exit
