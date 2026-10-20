@echo off
title Municipal Outage Triage Dashboard - IDA117V
echo ======================================================================
echo   STARTING MUNICIPAL OUTAGE TRIAGE GRADIO DASHBOARD (IDA117V)
echo ======================================================================
echo.
cd /d "%~dp0"
echo Opening web browser to http://127.0.0.1:7860 ...
start http://127.0.0.1:7860
echo.
echo Running Gradio application in Python...
echo (Keep this command prompt window open while presenting!)
echo.
python src/app.py
pause
