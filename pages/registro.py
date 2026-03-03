"""
============================================================================
CamBus - Página de Registro Manual de Vehículos
Centro de Distribución Mabe SLP
============================================================================
Registro manual de entrada y salida de vehículos
"""

import streamlit as st
import re
from datetime import datetime

from utils.db import (
    get_andenes_libres,
    get_andenes_ocupados,
    get_camaras_anden,
    registrar_entrada_vehiculo,
    registrar_salida_vehiculo
)
from utils.auth import get_current_user, require_role


# Tipos de vehículos
TIPOS_VEHICULO = ['TORTON', 'RABON', 'FULL', 'CAMIONETA']


def validar_placa(placa: str) -> tuple[bool, str]:
    """
    Valida el formato de una placa mexicana.
    
    Args:
        placa: Placa a validar
    
    Returns:
        Tuple (válida: bool, mensaje: str)
    """
    if not placa:
        return False, "La placa es requerida"
    
    # Limpiar placa
    placa_limpia = placa.upper().strip().replace(" ", "").replace("-", "")
    
    # Validar longitud
    if len(placa_limpia) < 5 or len(placa_limpia) > 8:
        return False, "Longitud de placa inválida"
    
    # Patrón básico para placas mexicanas
    patron = re.compile(r'^[A-Z0-9]{5,8}$')
    if not patron.match(placa_limpia):
        return False, "Formato de placa inválido"
    
    return True, placa_limpia


def render_tab_entrada():
    """Renderiza la pestaña de registro de entrada"""
    st.markdown("### 📥 Registrar Entrada de Vehículo")
    
    user = get_current_user()
    
    # Obtener andenes libres
    andenes_libres = get_andenes_libres()
    
    if not andenes_libres:
        st.warning("⚠️ No hay andenes disponibles en este momento")
        return
    
    with st.form("form_entrada", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Placa del vehículo
            placa = st.text_input(
                "Placa del Vehículo *",
                placeholder="ABC-123-A",
                help="Ingrese la placa del vehículo (se convertirá a mayúsculas)",
                max_chars=10
            ).upper()
            
            # Selector de andén
            andenes_opciones = {f"Andén {a['numero']}": a['id'] for a in andenes_libres}
            anden_seleccionado = st.selectbox(
                "Andén de Destino *",
                options=list(andenes_opciones.keys()),
                help="Seleccione el andén donde se ubicará el vehículo"
            )
            
            # Selector de cámara
            if anden_seleccionado:
                anden_id = andenes_opciones[anden_seleccionado]
                camaras = get_camaras_anden(anden_id)
                
                if camaras:
                    camaras_opciones = {f"{c['nombre']} - {c['ubicacion']}": c['id'] for c in camaras}
                    camara_seleccionada = st.selectbox(
                        "Cámara",
                        options=list(camaras_opciones.keys()),
                        help="Cámara que capturó la placa"
                    )
                    camara_id = camaras_opciones.get(camara_seleccionada)
                else:
                    st.info("No hay cámaras activas en este andén")
                    camara_id = None
            else:
                camara_id = None
        
        with col2:
            # Tipo de vehículo
            tipo_vehiculo = st.selectbox(
                "Tipo de Vehículo *",
                options=TIPOS_VEHICULO,
                help="Seleccione el tipo de vehículo"
            )
            
            # Transportista
            transportista = st.text_input(
                "Transportista",
                placeholder="Nombre de la empresa transportista",
                help="Empresa o persona que opera el vehículo"
            )
            
            # Confianza OCR
            confianza_ocr = st.number_input(
                "Confianza OCR (%)",
                min_value=0.0,
                max_value=100.0,
                value=98.5,
                step=0.1,
                help="Nivel de confianza del reconocimiento automático"
            )
        
        # Observaciones
        observaciones = st.text_area(
            "Observaciones",
            placeholder="Notas adicionales sobre el vehículo o la operación",
            max_chars=500
        )
        
        st.markdown("---")
        
        # Botón de registro
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button(
                "Registrar Entrada",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            # Validar placa
            placa_valida, placa_resultado = validar_placa(placa)
            
            if not placa_valida:
                st.error(f"❌ {placa_resultado}")
                return
            
            if not anden_seleccionado:
                st.error("❌ Debe seleccionar un andén")
                return
            
            # Registrar entrada
            with st.spinner("Registrando entrada..."):
                success, mensaje = registrar_entrada_vehiculo(
                    placa=placa_resultado,
                    anden_id=andenes_opciones[anden_seleccionado],
                    camara_id=camara_id or 1,  # Default si no hay cámara
                    tipo_vehiculo=tipo_vehiculo,
                    transportista=transportista,
                    confianza_ocr=confianza_ocr,
                    observaciones=observaciones,
                    usuario_id=user['id']
                )
                
                if success:
                    st.success(mensaje)
                    st.balloons()
                else:
                    st.error(mensaje)


def render_tab_salida():
    """Renderiza la pestaña de registro de salida"""
    st.markdown("### 📤 Registrar Salida de Vehículo")
    
    user = get_current_user()
    
    # Verificar si hay un registro de salida pendiente desde el dashboard
    registro_pendiente = st.session_state.get('registro_salida_id')
    
    # Obtener andenes ocupados
    andenes_ocupados = get_andenes_ocupados()
    
    if not andenes_ocupados:
        st.info("No hay vehículos en andenes actualmente")
        return
    
    # Crear opciones para el selector
    opciones = {
        f"Andén {a['numero']} - {a['placa']}": a 
        for a in andenes_ocupados
    }
    
    # Si hay un registro pendiente, preseleccionarlo
    indice_default = 0
    if registro_pendiente:
        for idx, (_, data) in enumerate(opciones.items()):
            if data['registro_id'] == registro_pendiente:
                indice_default = idx
                break
        # Limpiar el registro pendiente
        st.session_state.pop('registro_salida_id', None)
    
    # Selector de andén/vehículo
    seleccion = st.selectbox(
        "Seleccionar Vehículo a Registrar Salida",
        options=list(opciones.keys()),
        index=indice_default,
        help="Seleccione el vehículo que está saliendo"
    )
    
    if seleccion:
        datos = opciones[seleccion]
        
        # Mostrar información del vehículo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Andén", datos['numero'])
        with col2:
            st.metric("Placa", datos['placa'])
        with col3:
            st.metric("ID Registro", datos['registro_id'])
        
        st.markdown("---")
        
        # Confirmación de salida
        st.warning("⚠️ Al registrar la salida, el andén quedará disponible.")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button(
                "Confirmar Salida",
                use_container_width=True,
                type="primary"
            ):
                with st.spinner("Registrando salida..."):
                    success, mensaje, duracion = registrar_salida_vehiculo(
                        registro_id=datos['registro_id'],
                        usuario_id=user['id']
                    )
                    
                    if success:
                        st.success(mensaje)
                        
                        # Mostrar resumen
                        if duracion:
                            horas = int(duracion // 60)
                            minutos = int(duracion % 60)
                            st.info(f"⏱️ Tiempo de estancia: {horas}h {minutos}m ({duracion:.1f} minutos)")
                        
                        st.balloons()
                        # Recargar para actualizar la lista
                        st.rerun()
                    else:
                        st.error(mensaje)


def render_registro():
    """Renderiza la página completa de registro"""
    st.markdown("## Registro Manual de Vehículos")
    st.caption("Registre manualmente la entrada o salida de vehículos")
    
    st.markdown("---")
    
    # Crear pestañas
    tab1, tab2 = st.tabs(["Registrar Entrada", "Registrar Salida"])
    
    with tab1:
        render_tab_entrada()
    
    with tab2:
        render_tab_salida()
