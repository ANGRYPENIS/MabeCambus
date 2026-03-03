#!/bin/bash

# ============================================================================
# CamBus - Script para Git Commit y Push
# Centro de Distribución Mabe SLP
# ============================================================================

clear
echo ""
echo "=========================================="
echo "CamBus - Git Commit y Push"
echo "Centro de Distribución Mabe SLP"
echo "=========================================="
echo ""

# Verificar que Git está instalado
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git no encontrado"
    echo "Instala desde: https://git-scm.com/download"
    echo ""
    exit 1
fi

echo "Estado actual del repositorio:"
echo ""
git status --short

echo ""
read -p "Mensaje de commit (por defecto 'Update'): " MENSAJE
if [ -z "$MENSAJE" ]; then
    MENSAJE="Update"
fi

echo ""
echo "[*] Agregando archivos..."
git add .

echo "[*] Haciendo commit..."
git commit -m "$MENSAJE"
if [ $? -ne 0 ]; then
    echo "[ADVERTENCIA] No hay cambios para hacer commit"
    exit 0
fi

echo "[*] Haciendo push a GitHub..."
git push
if [ $? -ne 0 ]; then
    echo "[ERROR] No se pudo hacer push"
    echo "Verifica tu conexion y credenciales"
    exit 1
fi

echo ""
echo "=========================================="
echo "[✓] Cambios subidos a GitHub exitosamente"
echo "=========================================="
echo ""
