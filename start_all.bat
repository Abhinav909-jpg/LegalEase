@echo off
echo ==============================================
echo   Starting LegalEase (Backend + Frontend)
echo ==============================================

echo Launching Backend server on http://localhost:8000...
start "LegalEase Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo Launching Frontend dev server on http://localhost:5173...
start "LegalEase Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers are launching in separate windows!
echo Once ready, open your browser at: http://localhost:5173
echo.
pause
