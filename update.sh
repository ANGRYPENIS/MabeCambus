#!/bin/bash

# ============================================================================
# CamBus - Script de Actualización para Linux/Mac
# Centro de Distribución Mabe SLP
# ============================================================================

clear
echo ""
echo "=========================================="
echo "CamBus - Actualizar Aplicacion"
echo "Centro de Distribución Mabe SLP"
echo "=========================================="
echo ""

# Verificar que existe venv
if [ ! -d "venv" ]; then
    echo "[ERROR] Entorno virtual no encontrado"
    echo "Debes ejecutar setup.sh primero"
    echo ""
    exit 1
fi

# Activar venv
echo "[1/3] Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] No se pudo activar el entorno virtual"
    exit 1
fi
echo "[✓] Entorno virtual activado"

# Verificar si existe git
if ! command -v git &> /dev/null; then
    echo "[ADVERTENCIA] Git no encontrado, saltando actualizacion de codigo"
    echo "             (Git no es requerido, solo opcional)"
    GIT_AVAILABLE=0
else
    echo "[2/3] Actualizando codigo desde Git..."
    git pull origin main
    if [ $? -ne 0 ]; then
        echo "[ADVERTENCIA] No se pudo actualizar desde Git"
        echo "             Asegúrate de tener permisos y conexion"
    else
        echo "[✓] Codigo actualizado"
    fi
    GIT_AVAILABLE=1
fi

# Actualizar dependencias
if [ $GIT_AVAILABLE -eq 1 ]; then
    PASO=3
else
    PASO=2
fi
echo "[$PASO/3] Actualizando dependencias Python..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install --upgrade -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ADVERTENCIA] Algunos paquetes no se actualizaron correctamente"
    echo "             Intenta ejecutar: pip install -r requirements.txt"
else
    echo "[✓] Todas las dependencias actualizadas"
fi

echo ""
echo "=========================================="
echo "ACTUALIZACION COMPLETADA"
echo "=========================================="
echo ""
echo "Puedes ejecutar: ./run.sh"
echo ""
