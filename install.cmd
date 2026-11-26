@echo off
py -3 "%~dp0install.py"
if errorlevel 1 exit /b 1
