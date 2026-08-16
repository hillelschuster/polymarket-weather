@echo off
cd /d "%~dp0"
if not exist data mkdir data
echo Starting live trader (DRY_RUN until .env flips it live). Logs: data\run.log
start "weather-trader" /min cmd /c "python -u scripts\live_trader.py >NUL 2>&1"
echo Started in background window "weather-trader". To stop: close that window.
