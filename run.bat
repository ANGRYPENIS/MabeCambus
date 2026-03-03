@echo off
REM ============================================================================
REM CamBus - Script para Ejecutar la Aplicacion
REM Centro de Distribución Mabe SLP
REM ============================================================================
setlocal enabledelayedexpansion

cls
echo.
echo ============================================================
echo   CamBus - Control de Acceso Vehicular
echo   Centro de Distribución Mabe SLP
echo ============================================================
echo.

REM Verificar que existe venv
if not exist venv (
    echo [ERROR] Entorno virtual no encontrado
    echo.
    echo Debes ejecutar setup.bat primero:
    echo   .\setup.bat
    echo.
    pause
    exit /b 1
)

REM Verificar que app.py existe
if not exist app.py (
    echo [ERROR] app.py no encontrado
    echo Asegúrate de que estás en la carpeta correcta
    echo.
    pause
    exit /b 1
)

REM Activar venv
echo [*] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)

REM Verificar PostgreSQL
echo [*] Verificando conexion a PostgreSQL...
python -c "import psycopg2; print('[OK] PostgreSQL disponible')" >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] No se pudo conectar a PostgreSQL
    echo Asegúrate que:
    echo   1. PostgreSQL está instalado y corriendo
    echo   2. El puerto 5432 está disponible
    echo   3. Las credenciales en .env son correctas
    echo.
    set /p CONTINUAR="¿Continuar de todas formas [S/N]? "
    if /i not "!CONTINUAR!"=="S" (
        echo Abortado
        pause
        exit /b 1
    )
)

echo.
echo ============================================================
echo   INICIANDO CAMBUS
echo ============================================================
echo.
echo La aplicación se abrirá en: http://localhost:8501
echo.
echo Para detener, presiona: CTRL+C
echo.
echo ============================================================
echo.

REM Ejecutar streamlit
streamlit run app.py

REM Si streamlit se detiene, mostrar mensaje
if errorlevel 1 (
    echo.
    echo [ERROR] La aplicacion se detuvo inesperadamente
    echo Revisa los errores arriba para más detalles
    echo.
)

pause
