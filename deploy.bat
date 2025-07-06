@echo off
echo ======================================
echo Voodo Server Deployment Script
echo ======================================

echo Building Docker image...
docker build -t voodo-server .

echo Starting server containers...
docker-compose up -d

echo Server deployment complete!
echo Access the API at http://localhost:5000/docs
