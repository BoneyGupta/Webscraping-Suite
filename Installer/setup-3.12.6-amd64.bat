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

echo Python 3.12.6 installed successfully and added to the PATH.
pause
exit /b
