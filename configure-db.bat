@echo off
REM =====================================================
REM CAMBUS - Database Configuration Script (Windows)
REM - Select or create PostgreSQL database
REM - Create new PostgreSQL user
REM - Initialize database with SQL schema
REM - Create demo user
REM =====================================================
setlocal enabledelayedexpansion

cls
color 0A
echo.
echo ================================
echo   CAMBUS Database Configuration
echo ================================
echo.

REM Verify PostgreSQL is installed
psql --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PostgreSQL not found on system
    echo Install from: https://www.postgresql.org/download/windows/
    echo.
    pause
    exit /b 1
)

echo MENU DE OPCIONES:
echo   1. Usar base de datos existente
echo   2. Crear nueva base de datos
echo   0. Salir
echo.

set /p choice="Selecciona una opcion (0-2): "

if "%choice%"=="0" goto :end
if "%choice%"=="1" goto :use_existing
if "%choice%"=="2" goto :create_new
echo Error: opcion no valida
timeout /t 2 >nul
goto :end

REM =====================================================
REM OPTION 1: USE EXISTING DATABASE
REM =====================================================
:use_existing
cls
echo Configuring with existing database...
echo.

set /p pg_host="PostgreSQL Host (default: localhost): " || set pg_host=localhost
if "!pg_host!"=="" set pg_host=localhost

set /p pg_port="PostgreSQL Port (default: 5432): " || set pg_port=5432
if "!pg_port!"=="" set pg_port=5432

set /p pg_user="PostgreSQL Username (default: postgres): " || set pg_user=postgres
if "!pg_user!"=="" set pg_user=postgres

setlocal disabledelayedexpansion
set /p pg_password="PostgreSQL Password: "
setlocal enabledelayedexpansion

if "!pg_password!"=="" (
    echo Error: Password cannot be empty
    timeout /t 2 >nul
    goto :end
)

REM Test connection
echo.
echo Verifying connection...
setlocal disabledelayedexpansion
set PGPASSWORD=!pg_password!
psql -h !pg_host! -p !pg_port! -U !pg_user! -c "SELECT 1;" >nul 2>&1
setlocal enabledelayedexpansion
if errorlevel 1 (
    echo Error: Cannot connect to PostgreSQL with provided credentials
    timeout /t 3 >nul
    goto :end
)

echo [OK] Connected successfully
echo.

REM List available databases
echo Available databases:
echo.
setlocal disabledelayedexpansion
set PGPASSWORD=!pg_password!
psql -h !pg_host! -p !pg_port! -U !pg_user! -l 2>nul | findstr /v "template0\|template1\|postgres" | findstr /v "^-"
setlocal enabledelayedexpansion

echo.
set /p db_name="Enter database name to use: "

if "!db_name!"=="" (
    echo Error: Database name cannot be empty
    timeout /t 2 >nul
    goto :end
)

REM Verify database exists
echo Verifying database exists...
setlocal disabledelayedexpansion
set PGPASSWORD=!pg_password!
psql -h !pg_host! -p !pg_port! -U !pg_user! -d !db_name! -c "SELECT 1;" >nul 2>&1
setlocal enabledelayedexpansion
if errorlevel 1 (
    echo Error: Database !db_name! does not exist
    timeout /t 3 >nul
    goto :end
)

REM Create/Update demo user
echo.
echo Creating/updating demo user...
setlocal disabledelayedexpansion
set PGPASSWORD=!pg_password!
psql -h !pg_host! -p !pg_port! -U !pg_user! -d !db_name! <<EOF >nul 2>&1
INSERT INTO usuarios (nombre_completo, email, username, password_hash, rol, activo, departamento)
VALUES ('Demo User', 'demo@cambus.local', 'demo', '$2b$12$YY7GWLRVHMPXkc9iOvN/NeHEbKKW6SH1lWHPEqPjKsHwSHVqXFU3G', 'OPERADOR', true, 'DEMOSTRACION')
ON CONFLICT (username) DO UPDATE SET activo=true;
EOF
setlocal enabledelayedexpansion

echo [OK] Demo user ready (username: demo, password: demo_password)

goto :save_env

REM =====================================================
REM OPTION 2: CREATE NEW DATABASE
REM =====================================================
:create_new
cls
echo Creating new database...
echo.

set /p pg_host="PostgreSQL Host (default: localhost): " || set pg_host=localhost
if "!pg_host!"=="" set pg_host=localhost

set /p pg_port="PostgreSQL Port (default: 5432): " || set pg_port=5432
if "!pg_port!"=="" set pg_port=5432

set /p pg_admin="PostgreSQL Admin/Superuser (default: postgres): " || set pg_admin=postgres
if "!pg_admin!"=="" set pg_admin=postgres

setlocal disabledelayedexpansion
set /p pg_admin_pass="PostgreSQL Admin Password: "
setlocal enabledelayedexpansion

if "!pg_admin_pass!"=="" (
    echo Error: Admin password cannot be empty
    timeout /t 2 >nul
    goto :end
)

REM Test admin connection
echo.
echo Verifying admin connection...
setlocal disabledelayedexpansion
set PGPASSWORD=!pg_admin_pass!
psql -h !pg_host! -p !pg_port! -U !pg_admin! -c "SELECT 1;" >nul 2>&1
setlocal enabledelayedexpansion
if errorlevel 1 (
    echo Error: Cannot connect as admin user
    timeout /t 3 >nul
    goto :end
)

echo [OK] Connected as admin
echo.

set /p db_name="Enter new database name: "
if "!db_name!"=="" (
    echo Error: Database name cannot be empty
    timeout /t 2 >nul
    goto :end
)

set /p db_user="Enter new PostgreSQL username: "
if "!db_user!"=="" (
    echo Error: Username cannot be empty
    timeout /t 2 >nul
    goto :end
)

setlocal disabledelayedexpansion
set /p db_user_pass="Enter password for new user: "
setlocal enabledelayedexpansion

if "!db_user_pass!"=="" (
    echo Error: Password cannot be empty
    timeout /t 2 >nul
    goto :end
)

REM Create user and database
echo.
echo Creating PostgreSQL user: !db_user!
setlocal disabledelayedexpansion
set PGPASSWORD=!pg_admin_pass!
psql -h !pg_host! -p !pg_port! -U !pg_admin! <<EOF >nul 2>&1
CREATE USER "!db_user!" WITH PASSWORD '!db_user_pass!';
ALTER USER "!db_user!" CREATEDB;
EOF
setlocal enabledelayedexpansion

echo [OK] User created
echo.

echo Creating database: !db_name!
setlocal disabledelayedexpansion
set PGPASSWORD=!pg_admin_pass!
psql -h !pg_host! -p !pg_port! -U !pg_admin! <<EOF >nul 2>&1
CREATE DATABASE "!db_name!" OWNER "!db_user!" ENCODING 'UTF8' CONNECTION LIMIT 100;
EOF
setlocal enabledelayedexpansion

echo [OK] Database created
echo.

REM Load SQL schema
echo Loading database schema from cambus.sql...

if not exist "cambus.sql" (
    echo Error: cambus.sql not found in current directory
    timeout /t 3 >nul
    goto :end
)

setlocal disabledelayedexpansion
set PGPASSWORD=!db_user_pass!
psql -h !pg_host! -p !pg_port! -U !db_user! -d !db_name! -f cambus.sql >nul 2>&1
setlocal enabledelayedexpansion

if errorlevel 1 (
    echo Warning: Some errors occurred while loading schema (this may be normal)
) else (
    echo [OK] Database schema loaded successfully
)

echo.
echo Creating demo user...
setlocal disabledelayedexpansion
set PGPASSWORD=!db_user_pass!
psql -h !pg_host! -p !pg_port! -U !db_user! -d !db_name! <<EOF >nul 2>&1
INSERT INTO usuarios (nombre_completo, email, username, password_hash, rol, activo, departamento)
VALUES ('Demo User', 'demo@cambus.local', 'demo', '$2b$12$YY7GWLRVHMPXkc9iOvN/NeHEbKKW6SH1lWHPEqPjKsHwSHVqXFU3G', 'OPERADOR', true, 'DEMOSTRACION');
EOF
setlocal enabledelayedexpansion

echo [OK] Demo user created (username: demo, password: demo_password)

REM Set variables for env file
set pg_user=!db_user!
set pg_password=!db_user_pass!

goto :save_env

REM =====================================================
REM SAVE .env FILE
REM =====================================================
:save_env
echo.
echo Validating database connection...
setlocal disabledelayedexpansion
set PGPASSWORD=!pg_password!
psql -h !pg_host! -p !pg_port! -U !pg_user! -d !db_name! -c "SELECT 1;" >nul 2>&1
setlocal enabledelayedexpansion
if errorlevel 1 (
    echo Error: Failed to validate database connection
    timeout /t 3 >nul
    goto :end
)

REM Backup existing .env
if exist ".env" (
    echo Backing up existing .env file...
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
    for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
    copy ".env" ".env.backup.!mydate!_!mytime!" >nul
)

REM Create .env file
echo Creating .env file...
(
    echo # CamBus Environment Configuration
    echo # Generated by configure-db.bat
    echo # Do not commit this file to version control
    echo.
    echo # Database Configuration
    echo DB_HOST=!pg_host!
    echo DB_PORT=!pg_port!
    echo DB_NAME=!db_name!
    echo DB_USER=!pg_user!
    echo DB_PASSWORD=!pg_password!
    echo.
    echo # Application Settings
    echo STREAMLIT_LOGGER_LEVEL=info
    echo STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false
    echo STREAMLIT_CLIENT_TOOLBAR_MODE=minimal
) > .env

echo [OK] .env file created

REM Print summary
echo.
echo ================================
echo Database Configuration Complete!
echo ================================
echo.
echo Database:  !db_name!
echo User:      !pg_user!
echo Host:      !pg_host!:!pg_port!
echo.
echo Demo account:
echo   Username: demo
echo   Password: demo_password
echo.
echo Next steps:
echo   1. setup.bat (install dependencies)
echo   2. run.bat (start application)
echo   3. Open http://localhost:8501
echo.

timeout /t 5 >nul
goto :end

:end
endlocal
exit /b 0
