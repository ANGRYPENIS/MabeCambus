#!/bin/bash

# ============================================================================
# CamBus - Script de Instalación para Linux/Mac
# Centro de Distribución Mabe SLP
# ============================================================================

clear
echo ""
echo "=========================================="
echo "CamBus - Instalación en Linux/Mac"
echo "Centro de Distribución Mabe SLP"
echo "=========================================="
echo ""

# Verificar Python
echo "[1/5] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 no encontrado. Instálalo con:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
    echo "  macOS: brew install python3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "[✓] Python $PYTHON_VERSION encontrado"

# Verificar PostgreSQL
echo "[2/5] Verificando PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "[ADVERTENCIA] PostgreSQL no encontrado"
    echo "Instálalo con:"
    echo "  Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "  macOS: brew install postgresql"
    PG_MISSING=1
else
    PG_VERSION=$(psql --version 2>&1 | awk '{print $3}')
    echo "[✓] PostgreSQL $PG_VERSION encontrado"
    PG_MISSING=0
fi

# Crear entorno virtual
echo "[3/5] Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "Entorno virtual ya existe, saltando..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] No se pudo crear el entorno virtual"
        exit 1
    fi
    echo "[✓] Entorno virtual creado"
fi

# Activar entorno virtual
echo "[4/5] Activando entorno virtual e instalando dependencias..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] No se pudo activar el entorno virtual"
    exit 1
fi

# Instalar dependencias
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] No se pudieron instalar las dependencias"
    echo "Intenta ejecutar manualmente: pip install -r requirements.txt"
    exit 1
fi
echo "[✓] Dependencias instaladas correctamente"

# Configurar .env
echo "[5/5] Configurando variables de entorno..."
if [ -f ".env" ]; then
    echo "[✓] Archivo .env ya existe"
else
    cp .env.example .env
    echo "[✓] Archivo .env creado desde .env.example"
fi

echo ""
echo "=========================================="
echo "INSTALACION COMPLETADA EXITOSAMENTE"
echo "=========================================="
echo ""

if [ $PG_MISSING -eq 1 ]; then
    echo "[ADVERTENCIA] PostgreSQL no está instalado"
    echo ""
    echo "IMPORTANTE: Antes de ejecutar la aplicacion debes:"
    echo "  1. Instalar PostgreSQL"
    echo "  2. Crear la BD: psql -U postgres -f cambus.sql"
    echo "  3. Editar .env con tu contraseña de PostgreSQL"
    echo ""
fi

echo "PROXIMOS PASOS:"
echo "  1. Edita .env con tus credenciales de PostgreSQL"
echo "  2. Asegúrate que PostgreSQL está corriendo"
echo "  3. Carga las tablas: psql -h localhost -U postgres -d cambus_db -f cambus.sql"
echo ""
echo "PARA EJECUTAR:"
echo "  - Opción 1: ./run.sh"
echo "  - Opción 2: streamlit run app.py"
echo ""
echo "Para actualizar en el futuro: ./update.sh"
echo "Para limpiar archivos temporales: ./clean.sh"
echo ""
