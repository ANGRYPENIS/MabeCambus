@echo off
REM ============================================================================
REM CamBus - Script para Git Commit y Push
REM Centro de Distribución Mabe SLP
REM ============================================================================
setlocal enabledelayedexpansion

cls
echo.
echo ============================================================
echo   CamBus - Git Commit y Push
echo   Centro de Distribución Mabe SLP
echo ============================================================
echo.

REM Verificar que Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git no encontrado
    echo Instala desde: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Estado actual del repositorio:
echo.
git status --short

echo.
set /p MENSAJE="Mensaje de commit (por defecto 'Update'): "
if "!MENSAJE!"=="" set MENSAJE=Update

echo.
echo [*] Agregando archivos...
git add .

echo [*] Haciendo commit...
git commit -m "!MENSAJE!"
if errorlevel 1 (
    echo [ADVERTENCIA] No hay cambios para hacer commit
    pause
    exit /b 0
)

echo [*] Haciendo push a GitHub...
git push
if errorlevel 1 (
    echo [ERROR] No se pudo hacer push
    echo Verifica tu conexion y credenciales
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   [✓] Cambios subidos a GitHub exitosamente
echo ============================================================
echo.
pause
