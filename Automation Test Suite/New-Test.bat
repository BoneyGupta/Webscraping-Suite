@echo off

:: Define source and target files
set "source=..\excel\Template.xlsx"
set "target=..\excel\Test.xlsx"

:: Check if the source file exists
if not exist "%source%" (
    echo The source file Template.xlsx does not exist.
    pause
    exit /b
)

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

:: Copy the Template.xlsx to Test.xlsx
copy "%source%" "%target%" >nul
if %errorLevel% NEQ 0 (
    echo Failed to copy Template.xlsx to Test.xlsx.
    pause
    exit /b
)

echo Successfully copied Template.xlsx to Test.xlsx.

:: Open the new Test.xlsx file
start "" "%target%"

exit
