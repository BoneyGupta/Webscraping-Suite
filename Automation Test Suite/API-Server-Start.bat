@echo off

:: Move to WebAPI directory
cd ../WebApi

:: Run main.py
echo Running main.py from the parent directory...
start  uvicorn main:app --reload

exit

