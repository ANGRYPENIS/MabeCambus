@echo off
REM ============================================================================
REM CamBus - Verificar PostgreSQL en Windows
REM Centro de Distribución Mabe SLP
REM ============================================================================

cls
echo.
echo ============================================================
echo   CamBus - Verificar PostgreSQL
echo   Centro de Distribución Mabe SLP
echo ============================================================
echo.

REM Verificar usando psql en PATH
echo [1/4] Verificando si psql está en PATH...
psql --version >nul 2>&1
if errorlevel 1 (
    echo [X] PostgreSQL NO encontrado en PATH
    set PG_IN_PATH=0
) else (
    for /f "tokens=3" %%i in ('psql --version 2^>^&1') do set PG_VERSION=%%i
    echo [✓] PostgreSQL !PG_VERSION! encontrado en PATH
    set PG_IN_PATH=1
)

REM Verificar servicio PostgreSQL
echo.
echo [2/4] Verificando servicio de PostgreSQL...
sc query postgresql* >nul 2>&1
if errorlevel 1 (
    echo [X] Servicio PostgreSQL NO encontrado
    set PG_SERVICE=0
) else (
    echo [✓] Servicio PostgreSQL encontrado
    REM Ver si está corriendo
    tasklist | findstr /i "postgres" >nul 2>&1
    if errorlevel 1 (
        echo    Estado: DETENIDO
        set PG_RUNNING=0
    ) else (
        echo    Estado: CORRIENDO
        set PG_RUNNING=1
    )
    set PG_SERVICE=1
)

REM Verificar carpeta de instalación
echo.
echo [3/4] Verificando carpeta de instalación...
if exist "C:\Program Files\PostgreSQL" (
    echo [✓] Carpeta encontrada: C:\Program Files\PostgreSQL
    dir "C:\Program Files\PostgreSQL" /ad
    set PG_FOLDER=1
) else (
    echo [X] Carpeta C:\Program Files\PostgreSQL NO existe
    if exist "C:\Program Files (x86)\PostgreSQL" (
        echo [✓] Carpeta encontrada: C:\Program Files (x86)\PostgreSQL
        dir "C:\Program Files (x86)\PostgreSQL" /ad
        set PG_FOLDER=1
    ) else (
        echo [X] PostgreSQL NO está instalado
        set PG_FOLDER=0
    )
)

REM Intentar conexión
echo.
echo [4/4] Intentando conectar a PostgreSQL...
psql -h localhost -U postgres -c "SELECT version();" >nul 2>&1
if errorlevel 1 (
    echo [X] No se puede conectar a PostgreSQL
    echo    Posibles causas:
    echo    - Servicio no está corriendo
    echo    - Contraseña incorrecta
    echo    - Puerto 5432 bloqueado
    set PG_CONNECT=0
) else (
    echo [✓] Conexión exitosa a PostgreSQL
    set PG_CONNECT=1
)

REM Resumen
echo.
echo ============================================================
echo                        RESUMEN
echo ============================================================
echo.
if !PG_IN_PATH! equ 1 (
    echo [✓] psql en PATH
) else (
    echo [X] psql NO en PATH
)

if !PG_SERVICE! equ 1 (
    if !PG_RUNNING! equ 1 (
        echo [✓] Servicio instalado y CORRIENDO
    ) else (
        echo [⚠️] Servicio instalado pero DETENIDO
    )
) else (
    echo [X] Servicio NO instalado
)

if !PG_FOLDER! equ 1 (
    echo [✓] Carpeta de instalación encontrada
) else (
    echo [X] Carpeta de instalación NO encontrada
)

if !PG_CONNECT! equ 1 (
    echo [✓] Conexión a PostgreSQL EXITOSA
) else (
    echo [X] Conexión a PostgreSQL FALLIDA
)

echo.
echo ============================================================

REM Diagnóstico final
if !PG_IN_PATH! equ 1 (
    if !PG_SERVICE! equ 1 (
        if !PG_CONNECT! equ 1 (
            echo.
            echo [SUCCESS] PostgreSQL está instalado y funcionando correctamente
            echo.
            pause
            exit /b 0
        ) else (
            echo.
            echo [WARNING] PostgreSQL está instalado pero no responde
            echo Soluciones:
            echo 1. Inicia el servicio: net start postgresql-x64-16
            echo 2. Verifica el puerto 5432 no esté bloqueado
            echo 3. Verifica la contraseña del usuario postgres
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo [ERROR] PostgreSQL no está instalado o no está en PATH
        echo Descarga desde: https://www.postgresql.org/download/windows/
        echo.
        pause
        exit /b 1
    )
) else (
    echo.
    echo [ERROR] PostgreSQL no está instalado
    echo Descarga desde: https://www.postgresql.org/download/windows/
    echo.
    pause
    exit /b 1
)
