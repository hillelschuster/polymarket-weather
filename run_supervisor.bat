@echo off
cd /d "%~dp0"
if not exist data mkdir data
echo Starting weather supervisor (detached). Logs: data\run.log
start "weather-supervisor" /min cmd /c "python -u scripts\supervisor.py >NUL 2>&1"
echo Started in background window "weather-supervisor". To stop: close that window or Task Manager ^> python.
