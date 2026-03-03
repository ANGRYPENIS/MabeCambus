@echo off
REM ============================================================================
REM CamBus - Script para Limpiar Archivos Temporales
REM Centro de Distribución Mabe SLP
REM ============================================================================
setlocal enabledelayedexpansion

cls
echo.
echo ============================================================
echo   CamBus - Limpiar Archivos Temporales
echo   Centro de Distribución Mabe SLP
echo ============================================================
echo.

set "CONFIRMACION="
set /p CONFIRMACION="¿Deseas limpiar caché y archivos temporales? [S/N] "

if /i not "!CONFIRMACION!"=="S" (
    echo Abortado
    echo.
    pause
    exit /b 0
)

echo.
echo [*] Limpiando archivos...
echo.

REM Limpiar caché de Python
if exist __pycache__ (
    echo [*] Eliminando __pycache__ de raiz...
    rmdir /s /q __pycache__ >nul 2>&1
    echo [✓] Eliminado
)

REM Limpiar caché en utils
if exist utils\__pycache__ (
    echo [*] Eliminando __pycache__ de utils...
    rmdir /s /q utils\__pycache__ >nul 2>&1
    echo [✓] Eliminado
)

REM Limpiar caché en components
if exist components\__pycache__ (
    echo [*] Eliminando __pycache__ de components...
    rmdir /s /q components\__pycache__ >nul 2>&1
    echo [✓] Eliminado
)

REM Limpiar caché en pages
if exist pages\__pycache__ (
    echo [*] Eliminando __pycache__ de pages...
    rmdir /s /q pages\__pycache__ >nul 2>&1
    echo [✓] Eliminado
)

REM Limpiar caché de Streamlit
if exist .streamlit (
    echo [*] Eliminando cache de Streamlit (.streamlit)...
    rmdir /s /q .streamlit >nul 2>&1
    echo [✓] Eliminado
)

REM Limpiar .streamlit cache directory
for /d %%A in ("%appdata%\Streamlit") do (
    if exist "%%A" (
        echo [*] Eliminando cache global de Streamlit...
        rmdir /s /q "%%A" >nul 2>&1
        echo [✓] Eliminado
    )
)

REM Limpiar pytest cache si existe
if exist .pytest_cache (
    echo [*] Eliminando cache de pytest...
    rmdir /s /q .pytest_cache >nul 2>&1
    echo [✓] Eliminado
)

REM Limpiar .eggs
if exist .eggs (
    echo [*] Eliminando .eggs...
    rmdir /s /q .eggs >nul 2>&1
    echo [✓] Eliminado
)

REM Limpiar archivos .pyc
echo [*] Eliminando archivos .pyc...
for /r %%F in (*.pyc) do (
    del /q "%%F" >nul 2>&1
)
echo [✓] Eliminados

echo.
echo ============================================================
echo   LIMPIEZA COMPLETADA
echo ============================================================
echo.
echo Archivos limpios:
echo   - __pycache__ (en todas las carpetas)
echo   - Cache de Streamlit
echo   - Cache de pytest
echo   - Archivos .pyc
echo.
echo La proxima vez que ejecutes la app será más lenta (recompila)
echo pero usará menos espacio en disco.
echo.
pause
