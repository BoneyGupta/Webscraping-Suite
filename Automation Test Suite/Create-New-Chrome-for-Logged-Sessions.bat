@echo off

:: Step 1: Install Chrome Browser (this assumes the Chrome installer is in the same directory as the batch file)
set CHROME_INSTALLER=..\\Installer\\ChromeSetup.exe

:: Check if the Chrome installer exists
if not exist %CHROME_INSTALLER% (
    echo Chrome installer not found! Ensure %CHROME_INSTALLER% is in the same directory as this script.
    pause
    exit /b
)

echo Installing Google Chrome...
:: start /wait %CHROME_INSTALLER% /silent /install

:: Step 2: Copy Chrome folder to your directory
set SOURCE_DIR="C:\\Program Files\\Google\\Chrome\\Application"
set DEST_DIR="%~dp0..\\Application"

:: Check if Chrome directory exists
if not exist %SOURCE_DIR% (
    echo Chrome is not installed in the default directory.
    echo Searchin Chrome in User Profile
    set SOURCE_DIR="%USERPROFILE%\\AppData\\Local\\Google\\Chrome\\Application"
)

:: Check if Chrome directory exists
if not exist %SOURCE_DIR% (
    echo Chrome is not installed in the default directory.
    pause
    exit /b
)

echo Copying Chrome folder to your directory...
xcopy /e /i /h /y %SOURCE_DIR% %DEST_DIR%

:: Open command line and run Chrome with remote debugging
echo Launching Chrome with remote debugging on port 9988...
start "" "..\Application\chrome.exe" --remote-debugging-port=9988 --user-data-dir="..\\chromedata"

echo Chrome has been launched with remote debugging.
exit
