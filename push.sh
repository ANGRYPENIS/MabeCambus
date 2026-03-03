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

# Intentar hacer push, si falla por non-fast-forward, hacer pull y retry
echo "[*] Haciendo push a GitHub..."
git push
if [ $? -ne 0 ]; then
    echo ""
    echo "[⚠️  ADVERTENCIA] El push fue rechazado"
    echo "Posible causa: GitHub tiene cambios que no están locales"
    echo ""
    echo "[*] Intentando sincronizar cambios remotos..."
    echo "[*] Intento 1: Pull con --allow-unrelated-histories..."
    git pull origin main --allow-unrelated-histories --no-edit
    if [ $? -ne 0 ]; then
        echo "[ADVERTENCIA] Primer intento fallo, intentando con --no-rebase..."
        git pull origin main --no-rebase
        if [ $? -ne 0 ]; then
            echo "[ERROR] No se pudo hacer pull"
            echo "Resuelve los conflictos manualmente:"
            echo "  1. git status (ver qué cambió)"
            echo "  2. Edita los archivos con conflictos"
            echo "  3. git add ."
            echo "  4. git commit -m \"Merge: resolver conflictos\""
            echo "  5. git push"
            exit 1
        fi
    fi
    
    echo "[*] Reintentando push..."
    git push
    if [ $? -ne 0 ]; then
        echo "[ERROR] Aún fallo el push después de pull"
        echo "Soluciones:"
        echo "  1. Revisa los conflictos manualmente: git status"
        echo "  2. Resuelve conflictos si los hay"
        echo "  3. Intenta: git push --force (¡cuidado!)"
        exit 1
    fi
fi

echo ""
echo "=========================================="
echo "[✓] Cambios subidos a GitHub exitosamente"
echo "=========================================="
echo ""

