@echo off
cd /d "%~dp0"
for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%a
robocopy data "data_backup\%TS%" /E /NJH /NJS /NDL /NFL >NUL
powershell -NoProfile -Command "Get-ChildItem 'data_backup' -Directory | Sort-Object Name -Descending | Select-Object -Skip 14 | Remove-Item -Recurse -Force"
echo Backup data_backup\%TS% done.
