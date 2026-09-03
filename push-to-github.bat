@echo off
REM ============================================================================
REM Push to GitHub & Setup Workflows (Windows Batch)
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo Push to GitHub Script (Windows)
echo ==========================================
echo.

if "%1"=="" (
    echo Usage: push-to-github.bat GITHUB_USERNAME
    echo.
    echo Example: push-to-github.bat johndoe
    echo.
    echo Steps to get your GitHub username:
    echo   1. Go to github.com
    echo   2. Click your profile icon (top right)
    echo   3. Click 'Your profile'
    echo   4. Your username is in the URL: github.com/YOUR_USERNAME
    echo.
    pause
    exit /b 1
)

set GITHUB_USERNAME=%1
set REPO_NAME=ai-options-trader

echo GitHub Username: !GITHUB_USERNAME!
echo Repository: !REPO_NAME!
echo.

REM ========================================================================
REM Step 1: Verify files
REM ========================================================================

echo Step 1: Verifying files...
echo.

set MISSING_FILES=0

if exist ".github\workflows\deploy.yml" (
    echo ^✓ .github\workflows\deploy.yml
) else (
    echo ^✗ .github\workflows\deploy.yml (MISSING^)
    set /a MISSING_FILES+=1
)

if exist ".github\scripts\market_monitor.py" (
    echo ^✓ .github\scripts\market_monitor.py
) else (
    echo ^✗ .github\scripts\market_monitor.py (MISSING^)
    set /a MISSING_FILES+=1
)

if exist ".gitignore" (
    echo ^✓ .gitignore
) else (
    echo ^✗ .gitignore (MISSING^)
    set /a MISSING_FILES+=1
)

if exist "backend\main.py" (
    echo ^✓ backend\main.py
) else (
    echo ^✗ backend\main.py (MISSING^)
    set /a MISSING_FILES+=1
)

if exist "docker-compose.yml" (
    echo ^✓ docker-compose.yml
) else (
    echo ^✗ docker-compose.yml (MISSING^)
    set /a MISSING_FILES+=1
)

if exist "requirements.txt" (
    echo ^✓ requirements.txt
) else (
    echo ^✗ requirements.txt (MISSING^)
    set /a MISSING_FILES+=1
)

echo.

if !MISSING_FILES! gtr 0 (
    echo Missing !MISSING_FILES! required files^^!
    echo Please ensure you're in the correct directory.
    pause
    exit /b 1
)

echo ^✓ All required files present
echo.

REM ========================================================================
REM Step 2: Initialize Git
REM ========================================================================

echo Step 2: Initializing Git repository...
echo.

if not exist ".git" (
    echo Initializing new repository...
    git init
    echo ^✓ Git initialized
) else (
    echo ^⚠ Git repository already exists
)

echo.

REM ========================================================================
REM Step 3: Configure Git
REM ========================================================================

echo Step 3: Configuring Git...
echo.

git config user.name > nul 2>&1
if errorlevel 1 (
    echo Git user not configured. Enter your details:
    set /p git_name="Name: "
    set /p git_email="Email: "
    git config user.name "!git_name!"
    git config user.email "!git_email!"
    echo ^✓ Git configured
) else (
    echo ^✓ Git already configured
    for /f "tokens=*" %%A in ('git config user.name') do set GIT_NAME=%%A
    echo    Name: !GIT_NAME!
)

echo.

REM ========================================================================
REM Step 4: Check remote
REM ========================================================================

echo Step 4: Setting up remote...
echo.

set REMOTE_URL=https://github.com/!GITHUB_USERNAME!/!REPO_NAME!.git

git remote get-url origin > nul 2>&1
if errorlevel 1 (
    echo Adding remote...
    git remote add origin "!REMOTE_URL!"
    echo ^✓ Remote added: !REMOTE_URL!
) else (
    echo ^✓ Remote already configured
)

echo.

REM ========================================================================
REM Step 5: Add and commit
REM ========================================================================

echo Step 5: Adding and committing files...
echo.

git status --porcelain | findstr . > nul
if errorlevel 1 (
    echo ^⚠ No changes to commit
    echo Repository is up to date
) else (
    echo Adding files...
    git add .

    echo Creating commit...
    git commit -m "Initial commit: AI Options Trading Platform Phase 1"

    echo ^✓ Files committed
)

echo.

REM ========================================================================
REM Step 6: Rename branch
REM ========================================================================

echo Step 6: Preparing branch...
echo.

for /f "tokens=*" %%A in ('git rev-parse --abbrev-ref HEAD') do set BRANCH=%%A

if not "!BRANCH!"=="main" (
    echo Renaming branch to 'main'...
    git branch -M main
    echo ^✓ Branch renamed to 'main'
) else (
    echo ^✓ Already on 'main' branch
)

echo.

REM ========================================================================
REM Step 7: Push to GitHub
REM ========================================================================

echo Step 7: Pushing to GitHub...
echo.
echo Repository URL: !REMOTE_URL!
echo.
echo ^⚠ You may be prompted for GitHub credentials:
echo    - Enter your GitHub username
echo    - Enter your personal access token (or password)
echo.
echo To create a personal access token:
echo   1. Go to github.com/settings/tokens
echo   2. Click 'Generate new token'
echo   3. Select 'repo' scope
echo   4. Copy and paste the token when prompted
echo.

git push -u origin main

if errorlevel 1 (
    echo ^✗ Push failed
    pause
    exit /b 1
)

echo.
echo ^✓ Code pushed to GitHub successfully^^!
echo.

REM ========================================================================
REM Summary
REM ========================================================================

echo ==========================================
echo ^✓ PUSH COMPLETE^^!
echo ==========================================
echo.
echo Repository: https://github.com/!GITHUB_USERNAME!/!REPO_NAME!
echo.
echo Next steps:
echo.
echo 1. Go to your repository:
echo    https://github.com/!GITHUB_USERNAME!/!REPO_NAME!
echo.
echo 2. Go to 'Actions' tab to see workflows running:
echo    https://github.com/!GITHUB_USERNAME!/!REPO_NAME!/actions
echo.
echo 3. Wait for workflows to complete:
echo    ^✓ test-and-lint
echo    ^✓ build-docker
echo    ^✓ market-monitor
echo    ^✓ deployment-check
echo.
echo 4. (Optional) Configure Slack notifications:
echo    Settings ^→ Secrets ^→ New secret
echo    Name: SLACK_WEBHOOK
echo    Value: ^<your slack webhook URL^>
echo.
echo 5. Read: GITHUB_ONLY_SETUP.md
echo.
echo ==========================================
echo.

pause
