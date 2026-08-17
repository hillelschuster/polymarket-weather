@echo off
cd /d "%~dp0"
if not exist data mkdir data
set "PY=python"
if exist "%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts\python.exe" set "PY=%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts\python.exe"
echo Starting live trader (DRY_RUN until .env flips it live). Logs: data\run.log
start "weather-trader" /min "%PY%" -u scripts\live_trader.py
echo Started in background window "weather-trader". To stop: close that window.
