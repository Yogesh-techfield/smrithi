@echo off
title SmritiSathi - Microservices & AWS EC2 Deployment
color 0b

echo ========================================================
echo        SMRITISATHI - CLOUD & DEVOPS PROJECT (INT 378)
echo ========================================================
echo Student: Yogesh (12307093)
echo Project: SIH26003 - Cognitive Care Platform for NER
echo Owner Email: yogyatha12345@gmail.com
echo ========================================================
echo.

cd /d "C:\Users\ASUS\.gemini\antigravity\scratch\smrithi"

echo [1/4] Checking Docker status...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Docker daemon is not responding yet.
    echo Please make sure Docker Desktop is open and running on your laptop.
) else (
    echo [SUCCESS] Docker is running!
    echo.
    echo [2/4] Building and launching microservices via Docker Compose...
    docker-compose up -d --build
    echo.
    echo [3/4] Verifying services health:
    curl -s http://localhost:5000/health
    echo.
    curl -s http://localhost:5001/health
    echo.
    curl -s http://localhost:5002/health
    echo.
)

echo.
echo ========================================================
echo [4/4] AWS EC2 Deployment via Terraform
echo ========================================================
echo You are logged in AWS in Chrome (yogyatha12345@gmail.com).
echo.
echo In AWS Console in Chrome:
echo 1. Click your username (top right) -^> Security credentials
echo 2. Scroll to 'Access keys' -^> Click 'Create access key'
echo 3. Enter them below:
echo.

set /p AWS_KEY="Enter AWS Access Key ID: "
if "%AWS_KEY%"=="" goto SkipAWS

set /p AWS_SECRET="Enter AWS Secret Access Key: "
set AWS_ACCESS_KEY_ID=%AWS_KEY%
set AWS_SECRET_ACCESS_KEY=%AWS_SECRET%
set AWS_DEFAULT_REGION=ap-south-1

cd terraform
echo.
echo Initializing Terraform...
terraform init
echo.
echo Deploying EC2 instance to AWS...
terraform apply -auto-approve

:SkipAWS
echo.
echo ========================================================
echo Application running at: http://localhost
echo All tasks executed.
echo ========================================================
pause
