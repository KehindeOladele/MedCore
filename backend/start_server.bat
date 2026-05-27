@echo off
title MedCore Backend Server
color 0A

echo.
echo  ==============================
echo    MedCore Backend Starting...
echo  ==============================
echo.
echo  Server will be available at:
echo  http://localhost:8000
echo  http://10.67.168.224:8000  (phone hotspot)
echo.
echo  Press Ctrl+C to stop the server.
echo  ==============================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo Server stopped. Press any key to close.
pause > nul
