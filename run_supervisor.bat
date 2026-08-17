@echo off
cd /d "%~dp0"
if not exist data mkdir data
set "PY=python"
if exist "%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts\python.exe" set "PY=%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts\python.exe"
echo Starting weather supervisor (detached). Logs: data\run.log
start "weather-supervisor" /min "%PY%" -u scripts\supervisor.py
echo Started in background window "weather-supervisor". To stop: close that window or Task Manager ^> python.
