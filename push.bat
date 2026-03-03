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

REM Intentar hacer push, si falla por non-fast-forward, hacer pull y retry
echo [*] Haciendo push a GitHub...
git push
if errorlevel 1 (
    echo.
    echo [⚠️  ADVERTENCIA] El push fue rechazado
    echo Posible causa: GitHub tiene cambios que no están locales
    echo.
    echo [*] Intentando sincronizar cambios remotos...
    echo [*] Intento 1: Pull con --allow-unrelated-histories...
    git pull origin main --allow-unrelated-histories --no-edit
    if errorlevel 1 (
        echo [ADVERTENCIA] Primer intento fallo, intentando con --no-rebase...
        git pull origin main --no-rebase
        if errorlevel 1 (
            echo [ERROR] No se pudo hacer pull
            echo Resuelve los conflictos manualmente:
            echo   1. git status (ver qué cambió)
            echo   2. Edita los archivos con conflictos
            echo   3. git add .
            echo   4. git commit -m "Merge: resolver conflictos"
            echo   5. git push
            pause
            exit /b 1
        )
    )
    
    echo [*] Reintentando push...
    git push
    if errorlevel 1 (
        echo [ERROR] Aún fallo el push después de pull
        echo Soluciones:
        echo   1. Revisa los conflictos manualmente: git status
        echo   2. Resuelve conflictos si los hay
        echo   3. Intenta: git push --force (¡cuidado!)
        pause
        exit /b 1
    )
)

echo.
echo ============================================================
echo   [✓] Cambios subidos a GitHub exitosamente
echo ============================================================
echo.
pause
