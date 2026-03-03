@echo off
REM ============================================================================
REM CamBus - Script de Actualización para Windows
REM Centro de Distribución Mabe SLP
REM ============================================================================
setlocal enabledelayedexpansion

cls
echo.
echo ============================================================
echo   CamBus - Actualizar Aplicacion
echo   Centro de Distribución Mabe SLP
echo ============================================================
echo.

REM Verificar que existe venv
if not exist venv (
    echo [ERROR] Entorno virtual no encontrado
    echo Debes ejecutar setup.bat primero
    echo.
    pause
    exit /b 1
)

REM Activar venv
echo [1/3] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo [✓] Entorno virtual activado

REM Verificar si existe git
git --version >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] Git no encontrado, saltando actualizacion de codigo
    echo             (Git no es requerido, solo opcional)
    set GIT_AVAILABLE=0
) else (
    echo [2/3] Actualizando codigo desde Git...
    git pull origin main
    if errorlevel 1 (
        echo [ADVERTENCIA] No se pudo actualizar desde Git
        echo             Asegúrate de tener permisos y conexion
    ) else (
        echo [✓] Codigo actualizado
    )
    set GIT_AVAILABLE=1
)

REM Actualizar dependencias
if "!GIT_AVAILABLE!"=="1" (
    set PASO=3
) else (
    set PASO=2
)
echo [%PASO%/3] Actualizando dependencias Python...
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install --upgrade -r requirements.txt
if errorlevel 1 (
    echo [ADVERTENCIA] Algunos paquetes no se actualizaron correctamente
    echo             Intenta ejecutar: pip install -r requirements.txt
) else (
    echo [✓] Todas las dependencias actualizadas
)

echo.
echo ============================================================
echo   ACTUALIZACION COMPLETADA
echo ============================================================
echo.
echo Puedes ejecutar: .\run.bat
echo.
pause
