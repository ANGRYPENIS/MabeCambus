#!/bin/bash

# ============================================================================
# CamBus - Script para Limpiar Archivos Temporales
# Centro de Distribución Mabe SLP
# ============================================================================

clear
echo ""
echo "=========================================="
echo "CamBus - Limpiar Archivos Temporales"
echo "Centro de Distribución Mabe SLP"
echo "=========================================="
echo ""

read -p "¿Deseas limpiar caché y archivos temporales? [s/n] " CONFIRMACION

if [ "$CONFIRMACION" != "s" ] && [ "$CONFIRMACION" != "S" ]; then
    echo "Abortado"
    echo ""
    exit 0
fi

echo ""
echo "[*] Limpiando archivos..."
echo ""

# Limpiar caché de Python
if [ -d "__pycache__" ]; then
    echo "[*] Eliminando __pycache__ de raiz..."
    rm -rf __pycache__
    echo "[✓] Eliminado"
fi

# Limpiar caché en utils
if [ -d "utils/__pycache__" ]; then
    echo "[*] Eliminando __pycache__ de utils..."
    rm -rf utils/__pycache__
    echo "[✓] Eliminado"
fi

# Limpiar caché en components
if [ -d "components/__pycache__" ]; then
    echo "[*] Eliminando __pycache__ de components..."
    rm -rf components/__pycache__
    echo "[✓] Eliminado"
fi

# Limpiar caché en pages
if [ -d "pages/__pycache__" ]; then
    echo "[*] Eliminando __pycache__ de pages..."
    rm -rf pages/__pycache__
    echo "[✓] Eliminado"
fi

# Limpiar caché de Streamlit
if [ -d ".streamlit" ]; then
    echo "[*] Eliminando cache de Streamlit (.streamlit)..."
    rm -rf .streamlit
    echo "[✓] Eliminado"
fi

# Limpiar .streamlit cache directory (macOS/Linux)
if [ -d "$HOME/.streamlit" ]; then
    echo "[*] Eliminando cache global de Streamlit..."
    rm -rf "$HOME/.streamlit"
    echo "[✓] Eliminado"
fi

# Limpiar pytest cache si existe
if [ -d ".pytest_cache" ]; then
    echo "[*] Eliminando cache de pytest..."
    rm -rf .pytest_cache
    echo "[✓] Eliminado"
fi

# Limpiar .eggs
if [ -d ".eggs" ]; then
    echo "[*] Eliminando .eggs..."
    rm -rf .eggs
    echo "[✓] Eliminado"
fi

# Limpiar archivos .pyc
echo "[*] Eliminando archivos .pyc..."
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "[✓] Eliminados"

# Limpiar carpetas .egg-info
echo "[*] Eliminando carpetas .egg-info..."
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
echo "[✓] Eliminadas"

echo ""
echo "=========================================="
echo "LIMPIEZA COMPLETADA"
echo "=========================================="
echo ""
echo "Archivos limpios:"
echo "  - __pycache__ (en todas las carpetas)"
echo "  - Cache de Streamlit"
echo "  - Cache de pytest"
echo "  - Archivos .pyc"
echo "  - Carpetas .egg-info"
echo ""
echo "La proxima vez que ejecutes la app será más lenta (recompila)"
echo "pero usará menos espacio en disco."
echo ""
