@echo off
REM ============================================================================
REM CamBus - Script de Instalación para Windows
REM Centro de Distribución Mabe SLP
REM ============================================================================
setlocal enabledelayedexpansion

REM Color rojo para errores
color 0F
cls

echo.
echo ============================================================
echo   CamBus - Control de Acceso Vehicular
echo   Centro de Distribución Mabe SLP
echo ============================================================
echo.

REM Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python no encontrado en PATH
    echo.
    echo Soluciones:
    echo   1. Descargar desde: https://python.org/downloads/
    echo   2. IMPORTANTE: Marca la opcion "Add Python to PATH"
    echo   3. Reinicia esta terminal
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [✓] Python !PYTHON_VERSION! encontrado

REM Verificar PostgreSQL
echo [2/5] Verificando PostgreSQL...
psql --version >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] PostgreSQL no encontrado en PATH
    echo             Necesario para que funcione la aplicacion
    echo.
    set PG_MISSING=1
) else (
    for /f "tokens=3" %%i in ('psql --version 2^>^&1') do set PG_VERSION=%%i
    echo [✓] PostgreSQL !PG_VERSION! encontrado
    set PG_MISSING=0
)

REM Crear entorno virtual
echo [3/5] Creando entorno virtual...
if exist venv (
    echo Entorno virtual ya existe, saltando...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [✓] Entorno virtual creado
)

REM Activar entorno virtual
echo [4/5] Activando entorno virtual y instalando dependencias...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)

REM Instalar dependencias
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias
    echo Intenta ejecutar manualmente: pip install -r requirements.txt
    pause
    exit /b 1
)
echo [✓] Dependencias instaladas correctamente

REM Configurar .env
echo [5/5] Configurando variables de entorno...
if exist .env (
    echo [✓] Archivo .env ya existe
) else (
    copy .env.example .env >nul
    echo [✓] Archivo .env creado desde .env.example
)

echo.
echo ============================================================
echo   INSTALACION COMPLETADA EXITOSAMENTE
echo ============================================================
echo.

if "!PG_MISSING!"=="1" (
    echo [ADVERTENCIA] PostgreSQL no está instalado
    echo.
    echo IMPORTANTE: Antes de ejecutar la aplicacion debes:
    echo   1. Instalar PostgreSQL desde: https://postgresql.org/download/windows/
    echo   2. Crear la BD: psql -h localhost -U postgres -f cambus.sql
    echo   3. Editar .env con tu contraseña de PostgreSQL
    echo.
    echo Lee la guia: POSTGRESQL_WINDOWS.md
    echo.
)

echo PROXIMOS PASOS:
echo   1. Edita .env con tus credenciales de PostgreSQL
echo   2. Asegúrate que PostgreSQL está corriendo
echo   3. Carga las tablas: psql -h localhost -U postgres -d cambus_db -f cambus.sql
echo.
echo PARA EJECUTAR:
echo   - Opción 1: Doble-clic en run.bat
echo   - Opción 2: En la terminal: streamlit run app.py
echo   - Opción 3: En la terminal: .\run.bat
echo.
echo Para actualizar en el futuro: .\update.bat
echo Para limpiar archivos temporales: .\clean.bat
echo.
pause
