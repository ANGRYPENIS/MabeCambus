#!/bin/bash

# =====================================================
# CAMBUS - Database Configuration Script (Linux/Mac)
# - Select or create PostgreSQL database
# - Create new PostgreSQL user
# - Initialize database with SQL schema
# - Create demo user
# =====================================================

clear
echo ""
echo "================================"
echo "   CAMBUS Database Configuration"
echo "================================"
echo ""

# Verify PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "[ERROR] PostgreSQL not found"
    echo "Install with:"
    echo "  Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    echo "  macOS: brew install postgresql"
    echo ""
    exit 1
fi

echo "MENU DE OPCIONES:"
echo "  1. Usar base de datos existente"
echo "  2. Crear nueva base de datos"
echo "  0. Salir"
echo ""

read -p "Selecciona una opcion (0-2): " choice

case $choice in
    0)
        exit 0
        ;;
    1)
        use_existing_db
        ;;
    2)
        create_new_db
        ;;
    *)
        echo "Error: opcion no valida"
        sleep 2
        exit 1
        ;;
esac

# =====================================================
# OPTION 1: USE EXISTING DATABASE
# =====================================================
use_existing_db() {
    clear
    echo "Configuring with existing database..."
    echo ""
    
    read -p "PostgreSQL Host (default: localhost): " pg_host
    pg_host=${pg_host:-localhost}
    
    read -p "PostgreSQL Port (default: 5432): " pg_port
    pg_port=${pg_port:-5432}
    
    read -p "PostgreSQL Username (default: postgres): " pg_user
    pg_user=${pg_user:-postgres}
    
    read -sp "PostgreSQL Password: " pg_password
    echo ""
    
    if [ -z "$pg_password" ]; then
        echo "Error: Password cannot be empty"
        sleep 2
        exit 1
    fi
    
    # Test connection
    echo ""
    echo "Verifying connection..."
    PGPASSWORD="$pg_password" psql -h "$pg_host" -p "$pg_port" -U "$pg_user" -c "SELECT 1;" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error: Cannot connect to PostgreSQL with provided credentials"
        sleep 3
        exit 1
    fi
    
    echo "[OK] Connected successfully"
    echo ""
    
    # List available databases
    echo "Available databases:"
    echo ""
    PGPASSWORD="$pg_password" psql -h "$pg_host" -p "$pg_port" -U "$pg_user" -l -t 2>/dev/null | \
        awk -F'|' '($1 !~ /template/ && NF>0) {print $1}' | sed 's/^ *//;s/ *$//' | grep -v '^$' | nl
    
    echo ""
    read -p "Enter database name to use: " db_name
    
    if [ -z "$db_name" ]; then
        echo "Error: Database name cannot be empty"
        sleep 2
        exit 1
    fi
    
    # Verify database exists
    echo "Verifying database exists..."
    PGPASSWORD="$pg_password" psql -h "$pg_host" -p "$pg_port" -U "$pg_user" -d "$db_name" -c "SELECT 1;" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error: Database $db_name does not exist"
        sleep 3
        exit 1
    fi
    
    # Create/Update demo user
    echo ""
    echo "Creating/updating demo user..."
    PGPASSWORD="$pg_password" psql -h "$pg_host" -p "$pg_port" -U "$pg_user" -d "$db_name" <<EOF >/dev/null 2>&1
INSERT INTO usuarios (nombre_completo, email, username, password_hash, rol, activo, departamento)
VALUES ('Demo User', 'demo@cambus.local', 'demo', '\$2b\$12\$YY7GWLRVHMPXkc9iOvN/NeHEbKKW6SH1lWHPEqPjKsHwSHVqXFU3G', 'OPERADOR', true, 'DEMOSTRACION')
ON CONFLICT (username) DO UPDATE SET activo=true;
EOF
    
    echo "[OK] Demo user ready (username: demo, password: demo_password)"
    
    save_env_file
}

# =====================================================
# OPTION 2: CREATE NEW DATABASE
# =====================================================
create_new_db() {
    clear
    echo "Creating new database..."
    echo ""
    
    read -p "PostgreSQL Host (default: localhost): " pg_host
    pg_host=${pg_host:-localhost}
    
    read -p "PostgreSQL Port (default: 5432): " pg_port
    pg_port=${pg_port:-5432}
    
    read -p "PostgreSQL Admin/Superuser (default: postgres): " pg_admin
    pg_admin=${pg_admin:-postgres}
    
    read -sp "PostgreSQL Admin Password: " pg_admin_pass
    echo ""
    
    if [ -z "$pg_admin_pass" ]; then
        echo "Error: Admin password cannot be empty"
        sleep 2
        exit 1
    fi
    
    # Test admin connection
    echo ""
    echo "Verifying admin connection..."
    PGPASSWORD="$pg_admin_pass" psql -h "$pg_host" -p "$pg_port" -U "$pg_admin" -c "SELECT 1;" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error: Cannot connect as admin user"
        sleep 3
        exit 1
    fi
    
    echo "[OK] Connected as admin"
    echo ""
    
    read -p "Enter new database name: " db_name
    if [ -z "$db_name" ]; then
        echo "Error: Database name cannot be empty"
        sleep 2
        exit 1
    fi
    
    read -p "Enter new PostgreSQL username: " pg_user
    if [ -z "$pg_user" ]; then
        echo "Error: Username cannot be empty"
        sleep 2
        exit 1
    fi
    
    read -sp "Enter password for new user: " pg_password
    echo ""
    
    if [ -z "$pg_password" ]; then
        echo "Error: Password cannot be empty"
        sleep 2
        exit 1
    fi
    
    # Create user and database
    echo ""
    echo "Creating PostgreSQL user: $pg_user"
    PGPASSWORD="$pg_admin_pass" psql -h "$pg_host" -p "$pg_port" -U "$pg_admin" <<EOF >/dev/null 2>&1
CREATE USER "$pg_user" WITH PASSWORD '$pg_password';
ALTER USER "$pg_user" CREATEDB;
EOF
    
    echo "[OK] User created"
    echo ""
    
    echo "Creating database: $db_name"
    PGPASSWORD="$pg_admin_pass" psql -h "$pg_host" -p "$pg_port" -U "$pg_admin" <<EOF >/dev/null 2>&1
CREATE DATABASE "$db_name" OWNER "$pg_user" ENCODING 'UTF8' CONNECTION LIMIT 100;
EOF
    
    echo "[OK] Database created"
    echo ""
    
    # Load SQL schema
    echo "Loading database schema from cambus.sql..."
    
    if [ ! -f "cambus.sql" ]; then
        echo "Error: cambus.sql not found in current directory"
        sleep 3
        exit 1
    fi
    
    PGPASSWORD="$pg_password" psql -h "$pg_host" -p "$pg_port" -U "$pg_user" -d "$db_name" -f cambus.sql >/dev/null 2>&1
    
    if [ $? -ne 0 ]; then
        echo "Warning: Some errors occurred while loading schema (this may be normal)"
    else
        echo "[OK] Database schema loaded successfully"
    fi
    
    echo ""
    echo "Creating demo user..."
    PGPASSWORD="$pg_password" psql -h "$pg_host" -p "$pg_port" -U "$pg_user" -d "$db_name" <<EOF >/dev/null 2>&1
INSERT INTO usuarios (nombre_completo, email, username, password_hash, rol, activo, departamento)
VALUES ('Demo User', 'demo@cambus.local', 'demo', '\$2b\$12\$YY7GWLRVHMPXkc9iOvN/NeHEbKKW6SH1lWHPEqPjKsHwSHVqXFU3G', 'OPERADOR', true, 'DEMOSTRACION');
EOF
    
    echo "[OK] Demo user created (username: demo, password: demo_password)"
    
    save_env_file
}

# =====================================================
# SAVE .env FILE
# =====================================================
save_env_file() {
    echo ""
    echo "Validating database connection..."
    PGPASSWORD="$pg_password" psql -h "$pg_host" -p "$pg_port" -U "$pg_user" -d "$db_name" -c "SELECT 1;" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error: Failed to validate database connection"
        sleep 3
        exit 1
    fi
    
    # Backup existing .env
    if [ -f ".env" ]; then
        echo "Backing up existing .env file..."
        cp ".env" ".env.backup.$(date +%Y%m%d_%H%M%S)"
    fi
    
    # Create .env file
    echo "Creating .env file..."
    cat > .env << EOF
# CamBus Environment Configuration
# Generated by configure-db.sh
# Do not commit this file to version control

# Database Configuration
DB_HOST=$pg_host
DB_PORT=$pg_port
DB_NAME=$db_name
DB_USER=$pg_user
DB_PASSWORD=$pg_password

# Application Settings
STREAMLIT_LOGGER_LEVEL=info
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false
STREAMLIT_CLIENT_TOOLBAR_MODE=minimal
EOF
    
    echo "[OK] .env file created"
    
    # Print summary
    echo ""
    echo "================================"
    echo "Database Configuration Complete!"
    echo "================================"
    echo ""
    echo "Database:  $db_name"
    echo "User:      $pg_user"
    echo "Host:      $pg_host:$pg_port"
    echo ""
    echo "Demo account:"
    echo "   Username: demo"
    echo "   Password: demo_password"
    echo ""
    echo "Next steps:"
    echo "   1. ./setup.sh (install dependencies)"
    echo "   2. ./run.sh (start application)"
    echo "   3. Open http://localhost:8501"
    echo ""
}

# Run the appropriate function based on user choice
exit 0
