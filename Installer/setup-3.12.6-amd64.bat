@echo off

:: Check for administrative privileges
NET SESSION >nul 2>&1
if %errorLevel% NEQ 0 (
    echo This script requires administrative privileges. Please run it as an administrator.
    pause
    exit /b
)

:: Get the directory of the current batch file and change to that directory
cd /d "%~dp0"

:: Define the Python installer file
set PYTHON_INSTALLER=python-3.12.6-amd64.exe

:: Check if Python is already installed
python --version >nul 2>&1
if %errorLevel% EQU 0 (
    echo Python is already installed.
    goto skip_python_install
)

:: Check if the installer exists in the current directory
if not exist %PYTHON_INSTALLER% (
    echo Python installer not found! Ensure %PYTHON_INSTALLER% is in the same directory as this script.
    pause
    exit /b
)

:: Install Python for all users, add to PATH, and ensure pip is installed
echo Installing Python 3.12.6...
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1


:skip_python_install
:: Verify Python and pip installation
python --version
if %errorLevel% NEQ 0 (
    echo Python installation failed!
    pause
    exit /b
)

:: Continue with other installations

:: Install Playwright
echo Installing Playwright
start /wait pip install playwright 

if %errorLevel% NEQ 0 (
    echo Playwright installation failed!
    pause
    exit /b
)

:: Install openpyxl
echo Installing openpyxl
start /wait pip install openpyxl 

if %errorLevel% NEQ 0 (
    echo openpyxl installation failed!
    pause
    exit /b
)

:: Install xlwings
echo Installing xlwings
start /wait pip install xlwings 

if %errorLevel% NEQ 0 (
    echo xlwings installation failed!
    pause
    exit /b
)

:: Install Playwright browsers
echo Installing Playwright browsers...
start /wait playwright install

if %errorLevel% NEQ 0 (
    echo Playwright browser installation failed!
    pause
    exit /b
)

:: Install WebApi requirements.txt
echo WebApi libraries...
start /wait pip install -r ../WebApi/requirements.txt

if %errorLevel% NEQ 0 (
    echo WebApi requirements.txt failed!
    pause
    exit /b
)

echo Python 3.12.6 and its libraries installed successfully and added to the PATH.


setlocal

:: Step 1: Create a new folder named 'Automation Test Suite' on the Desktop
set "desktop=%USERPROFILE%\Desktop"
set "new_folder=%desktop%\Automation Test Suite"

if not exist "%new_folder%" (
    mkdir "%new_folder%"
    echo Created 'Automation Test Suite' folder on the Desktop.
) else (
    echo 'Automation Test Suite' folder already exists on the Desktop.
)

cd ..

:: Step 2: Create a shortcut for the 'Automation Test Suite' folder in the current directory inside 'Automation Test Suite'
set "ATS_folder=%CD%\Automation Test Suite"
set "shortcut_ATS=%new_folder%\Automation Test Suite.lnk"

if exist "%ATS_folder%" (
    echo Creating shortcut for the 'Automation Test Suite' folder from current directory...
    powershell "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%shortcut_ATS%'); $s.TargetPath = '%ATS_folder%'; $s.Save()"
    echo Shortcut to 'Automation Test Suite' folder created.
) else (
    echo 'Automation Test Suite' folder does not exist in the current directory.
)


:: Define source and target files
set "source=excel archives\Template.xlsx"
set "target=excel\Test.xlsx"

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

pause
exit /b
