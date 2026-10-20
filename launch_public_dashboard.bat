@echo off
title Municipal Outage Triage Dashboard (Public Share Link) - IDA117V
echo ======================================================================
echo   STARTING GRADIO DASHBOARD WITH PUBLIC SHAREABLE LINK (GRADIO LIVE)
echo ======================================================================
echo.
cd /d "%~dp0"
echo Generating secure public HTTPS link for external devices/markers...
echo (A public gradio.live URL will be generated below)
echo.
python src/app.py --share
pause
