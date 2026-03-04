#!/bin/bash

# ============================================================================
# CamBus - Verificar PostgreSQL en Linux/Mac
# Centro de Distribución Mabe SLP
# ============================================================================

clear
echo ""
echo "=========================================="
echo "CamBus - Verificar PostgreSQL"
echo "Centro de Distribución Mabe SLP"
echo "=========================================="
echo ""

PG_IN_PATH=0
PG_SERVICE=0
PG_CONNECT=0

# Verificar usando psql en PATH
echo "[1/4] Verificando si psql está en PATH..."
if ! command -v psql &> /dev/null; then
    echo "[X] PostgreSQL NO encontrado en PATH"
    PG_IN_PATH=0
else
    PG_VERSION=$(psql --version 2>&1 | awk '{print $3}')
    echo "[✓] PostgreSQL $PG_VERSION encontrado en PATH"
    PG_IN_PATH=1
fi

# Verificar si el servicio está corriendo
echo ""
echo "[2/4] Verificando si PostgreSQL está corriendo..."
if pgrep -x "postgres" > /dev/null; then
    echo "[✓] PostgreSQL está CORRIENDO"
    PG_SERVICE=1
else
    echo "[X] PostgreSQL NO está corriendo"
    PG_SERVICE=0
fi

# Verificar carpeta de instalación
echo ""
echo "[3/4] Verificando carpeta de instalación..."
if [ -d "/usr/lib/postgresql" ]; then
    echo "[✓] Carpeta encontrada: /usr/lib/postgresql"
    ls -d /usr/lib/postgresql/* 2>/dev/null | head -5
elif [ -d "/usr/local/Cellar/postgresql" ]; then
    echo "[✓] Carpeta encontrada: /usr/local/Cellar/postgresql (macOS)"
    ls -d /usr/local/Cellar/postgresql/* 2>/dev/null | head -5
else
    echo "[X] Carpeta de instalación NO encontrada"
fi

# Intentar conexión
echo ""
echo "[4/4] Intentando conectar a PostgreSQL..."
psql -h localhost -U postgres -c "SELECT version();" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[X] No se puede conectar a PostgreSQL"
    echo "   Posibles causas:"
    echo "   - Servicio no está corriendo"
    echo "   - Puerto 5432 bloqueado"
    echo "   - Usuario postgres no existe"
    PG_CONNECT=0
else
    echo "[✓] Conexión exitosa a PostgreSQL"
    PG_CONNECT=1
fi

# Resumen
echo ""
echo "=========================================="
echo "                RESUMEN"
echo "=========================================="
echo ""

if [ $PG_IN_PATH -eq 1 ]; then
    echo "[✓] psql en PATH"
else
    echo "[X] psql NO en PATH"
fi

if [ $PG_SERVICE -eq 1 ]; then
    echo "[✓] PostgreSQL está corriendo"
else
    echo "[X] PostgreSQL NO está corriendo"
fi

if [ $PG_CONNECT -eq 1 ]; then
    echo "[✓] Conexión a PostgreSQL EXITOSA"
else
    echo "[X] Conexión a PostgreSQL FALLIDA"
fi

echo ""
echo "=========================================="
echo ""

# Diagnóstico final
if [ $PG_IN_PATH -eq 1 ] && [ $PG_SERVICE -eq 1 ] && [ $PG_CONNECT -eq 1 ]; then
    echo "[SUCCESS] PostgreSQL está instalado y funcionando correctamente"
    echo ""
    exit 0
elif [ $PG_IN_PATH -eq 1 ] && [ $PG_SERVICE -eq 0 ]; then
    echo "[WARNING] PostgreSQL está instalado pero NO está corriendo"
    echo ""
    echo "Para iniciarlo:"
    echo "  • Linux (systemd): sudo systemctl start postgresql"
    echo "  • Linux (service): sudo service postgresql start"
    echo "  • macOS: brew services start postgresql"
    echo ""
    exit 1
else
    echo "[ERROR] PostgreSQL no está instalado"
    echo ""
    echo "Para instalarlo:"
    echo "  • Linux (Ubuntu/Debian): sudo apt install postgresql postgresql-contrib"
    echo "  • macOS: brew install postgresql"
    echo "  • Website: https://www.postgresql.org/download"
    echo ""
    exit 1
fi
