@echo off
TITLE HEXAKADAL Launcher
echo ========================================================
echo         ⚓ HEXAKADAL Commercial Decision Support System
echo ========================================================
echo.
echo [1] Start Vite Frontend only (Offline / Demo Mode)
echo [2] Start Spring Boot Backend + Vite Frontend (Full Stack)
echo [3] Build Frontend for Production (dist/)
echo.
set /p choice="Select an option (1, 2, or 3) [Default 1]: "
if "%choice%"=="" set choice=1

if "%choice%"=="1" goto frontend_only
if "%choice%"=="2" goto full_stack
if "%choice%"=="3" goto build_prod
goto frontend_only

:frontend_only
echo.
echo Starting Vite Frontend on http://localhost:5173 ...
cd frontend
start http://localhost:5173
call npm run dev
pause
exit

:full_stack
echo.
echo [1/2] Starting Spring Boot Backend on http://localhost:8081 ...
start "HEXAKADAL Backend" cmd /k "cd backend && mvn spring-boot:run"
echo.
echo Waiting 8 seconds for backend initialization...
timeout /t 8 /nobreak > nul
echo.
echo [2/2] Starting Vite Frontend on http://localhost:5173 ...
cd frontend
start http://localhost:5173
call npm run dev
pause
exit

:build_prod
echo.
echo Building production assets...
cd frontend
call npm run build
echo.
echo Build complete! Built files are in frontend/dist/
echo Starting preview server...
start http://localhost:4173
call npm run preview
pause
exit
