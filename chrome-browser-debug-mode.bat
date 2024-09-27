@echo off

:: Open command line and run Chrome with remote debugging
echo Launching Chrome with remote debugging on port 9988...
start "" "Application\chrome.exe" --remote-debugging-port=9988 --user-data-dir="..\\chromedata"

echo Chrome has been launched with remote debugging.
exit