#!/bin/bash

# ============================================================================
# CamBus - Script para Ejecutar la Aplicacion
# Centro de Distribución Mabe SLP
# ============================================================================

clear
echo ""
echo "=========================================="
echo "CamBus - Control de Acceso Vehicular"
echo "Centro de Distribución Mabe SLP"
echo "=========================================="
echo ""

# Verificar que existe venv
if [ ! -d "venv" ]; then
    echo "[ERROR] Entorno virtual no encontrado"
    echo ""
    echo "Debes ejecutar setup.sh primero:"
    echo "  ./setup.sh"
    echo ""
    exit 1
fi

# Verificar que app.py existe
if [ ! -f "app.py" ]; then
    echo "[ERROR] app.py no encontrado"
    echo "Asegúrate de que estás en la carpeta correcta"
    echo ""
    exit 1
fi

# Activar venv
echo "[*] Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] No se pudo activar el entorno virtual"
    exit 1
fi

# Verificar PostgreSQL
echo "[*] Verificando conexion a PostgreSQL..."
python3 -c "import psycopg2; print('[OK] PostgreSQL disponible')" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[ADVERTENCIA] No se pudo conectar a PostgreSQL"
    echo "Asegúrate que:"
    echo "  1. PostgreSQL está instalado y corriendo"
    echo "  2. El puerto 5432 está disponible"
    echo "  3. Las credenciales en .env son correctas"
    echo ""
    read -p "¿Continuar de todas formas [s/n]? " CONTINUAR
    if [ "$CONTINUAR" != "s" ] && [ "$CONTINUAR" != "S" ]; then
        echo "Abortado"
        exit 1
    fi
fi

echo ""
echo "=========================================="
echo "INICIANDO CAMBUS"
echo "=========================================="
echo ""
echo "La aplicación se abrirá en: http://localhost:8501"
echo ""
echo "Para detener, presiona: CTRL+C"
echo ""
echo "=========================================="
echo ""

# Ejecutar streamlit
streamlit run app.py

# Si streamlit se detiene, mostrar mensaje
if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] La aplicacion se detuvo inesperadamente"
    echo "Revisa los errores arriba para más detalles"
    echo ""
fi
