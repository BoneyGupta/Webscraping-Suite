@echo off

:: Move up one directory
cd ..

:: Run main.py
echo Running main.py from the parent directory...
start /wait python main.py

echo The run was completed.
exit
