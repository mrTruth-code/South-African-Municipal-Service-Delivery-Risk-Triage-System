@echo off
title Push Project to GitHub - IDA117V
echo ======================================================================
echo          PUSH IDA117V PROJECT REPOSITORY TO GITHUB
echo ======================================================================
echo.
cd /d "%~dp0"

echo Step 1: Please make sure you have created an empty repository on GitHub:
echo         Go to https://github.com/new and create a new repository.
echo         (Do NOT initialize with a README, .gitignore, or license)
echo.
set /p REPO_URL="Enter your GitHub Repository URL (e.g., https://github.com/username/repo.git): "

if "%REPO_URL%"=="" (
    echo Error: No repository URL entered. Aborting.
    pause
    exit /b
)

echo.
echo Setting remote origin to %REPO_URL% ...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main

echo.
echo Pushing committed files to GitHub branch 'main'...
git push -u origin main

echo.
echo ======================================================================
if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Your project has been pushed successfully to GitHub!
) else (
    echo [FAILED] Push failed. If prompted, please check your GitHub credentials or Personal Access Token.
)
echo ======================================================================
echo.
pause
