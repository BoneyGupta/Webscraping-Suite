@echo off

:: Move to WebAPI directory
cd ../WebApi

:: Run main.py
echo Running main.py from the parent directory...
start uvicorn main:app --host 127.0.0.1 --port 8001 --reload

timeout /t 5 /nobreak

start "" "http://127.0.0.1:8001/docs"

exit

