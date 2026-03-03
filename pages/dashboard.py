"""
============================================================================
CamBus - Página de Dashboard
Centro de Distribución Mabe SLP
============================================================================
Dashboard principal con KPIs, mapa de andenes y vehículos activos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

from utils.db import (
    get_dashboard_stats,
    get_andenes_estado,
    get_vehiculos_activos,
    get_top_andenes_tiempo
)
from utils.auth import has_permission, get_current_user


# Configuración de colores para estados de andenes
ESTADO_COLORES = {
    'LIBRE': '#28a745',      # Verde
    'OCUPADO': '#dc3545',    # Rojo
    'MANTENIMIENTO': '#ffc107',  # Amarillo
    'BLOQUEADO': '#343a40'   # Gris oscuro
}

ESTADO_ICONOS = {
    'LIBRE': '🟢',
    'OCUPADO': '🔴',
    'MANTENIMIENTO': '🟡',
    'BLOQUEADO': '⚫'
}


def render_kpis():
    """Renderiza las tarjetas de KPIs"""
    stats = get_dashboard_stats()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Andenes",
            value=stats['total_andenes'],
            help="Número total de andenes en el centro de distribución"
        )
    
    with col2:
        st.metric(
            label="🔴 Ocupados",
            value=stats['ocupados'],
            delta=None,
            help="Andenes actualmente ocupados"
        )
    
    with col3:
        st.metric(
            label="🟢 Libres",
            value=stats['libres'],
            delta=None,
            help="Andenes disponibles"
        )
    
    with col4:
        st.metric(
            label="Vehículos Hoy",
            value=stats['vehiculos_hoy'],
            help="Vehículos que han ingresado hoy"
        )
    
    with col5:
        st.metric(
            label="⏱️ Tiempo Promedio",
            value=f"{stats['tiempo_promedio']} min",
            help="Tiempo promedio de estancia hoy"
        )


def render_mapa_andenes():
    """Renderiza el mapa de andenes en grid 10x10"""
    st.markdown("### Mapa de Andenes en Tiempo Real")
    
    # Obtener estado de andenes
    andenes = get_andenes_estado()
    
    if not andenes:
        st.warning("No se pudieron cargar los andenes")
        return
    
    # Crear grid 10x10
    # Generar datos si no hay suficientes andenes
    if len(andenes) < 100:
        # Rellenar con andenes vacíos
        for i in range(len(andenes) + 1, 101):
            andenes.append({
                'id': i,
                'numero': i,
                'estado': 'LIBRE',
                'placa': None,
                'minutos': 0
            })
    
    # Leyenda
    st.markdown("""
    **Leyenda:** 🟢 Libre | 🔴 Ocupado | 🟡 Mantenimiento | ⚫ Bloqueado
    """)
    
    # Crear el grid usando columnas de Streamlit
    for row in range(10):
        cols = st.columns(10)
        for col_idx in range(10):
            anden_idx = row * 10 + col_idx
            if anden_idx < len(andenes):
                anden = andenes[anden_idx]
                
                with cols[col_idx]:
                    estado = anden.get('estado', 'LIBRE')
                    numero = anden.get('numero', anden_idx + 1)
                    placa = anden.get('placa', '')
                    minutos = anden.get('minutos', 0)
                    
                    # Icono según estado
                    icono = ESTADO_ICONOS.get(estado, '⚪')
                    
                    # Contenido del andén
                    if estado == 'OCUPADO' and placa:
                        content = f"""
                        <div style="
                            background-color: {ESTADO_COLORES.get(estado, '#gray')};
                            padding: 5px;
                            border-radius: 5px;
                            text-align: center;
                            min-height: 60px;
                            color: white;
                            font-size: 10px;
                        ">
                            <strong>{numero}</strong><br>
                            {placa[:7] if placa else ''}<br>
                            {int(minutos or 0)}m
                        </div>
                        """
                    else:
                        content = f"""
                        <div style="
                            background-color: {ESTADO_COLORES.get(estado, '#gray')};
                            padding: 5px;
                            border-radius: 5px;
                            text-align: center;
                            min-height: 60px;
                            color: white;
                            font-size: 12px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">
                            <strong>{numero}</strong>
                        </div>
                        """
                    
                    st.markdown(content, unsafe_allow_html=True)


def render_vehiculos_activos():
    """Renderiza la tabla de vehículos activos"""
    st.markdown("### Vehículos Activos")
    
    df = get_vehiculos_activos()
    
    if df.empty:
        st.info("No hay vehículos en andenes actualmente")
        return
    
    # Formatear datos
    df['hora_entrada'] = pd.to_datetime(df['hora_entrada']).dt.strftime('%H:%M:%S')
    df['tiempo'] = df['minutos'].apply(lambda x: f"{int(x)} min" if pd.notna(x) else "N/A")
    
    # Mostrar tabla
    user_can_register = has_permission(['ADMIN', 'SUPERVISOR'])
    
    # Crear tabla interactiva
    for idx, row in df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 2, 2, 2])
        
        with col1:
            st.write(f"**{row['anden']}**")
        with col2:
            st.write(row['placa'])
        with col3:
            st.write(row['hora_entrada'])
        with col4:
            st.write(row['tiempo'])
        with col5:
            st.write(row.get('tipo_operacion', 'N/A') or 'N/A')
        with col6:
            if user_can_register:
                if st.button("Salida", key=f"salida_{row['registro_id']}", help="Registrar salida"):
                    st.session_state.registro_salida_id = row['registro_id']
                    st.session_state.current_page = 'registro'
                    st.rerun()


def render_grafico_tiempos():
    """Renderiza el gráfico de barras de top 10 andenes por tiempo"""
    st.markdown("### Top 10 Andenes - Mayor Tiempo Promedio")
    
    df = get_top_andenes_tiempo()
    
    if df.empty:
        st.info("No hay datos suficientes para el gráfico")
        return
    
    # Crear gráfico con Plotly
    fig = px.bar(
        df,
        x='anden',
        y='tiempo_promedio',
        labels={'anden': 'Andén', 'tiempo_promedio': 'Tiempo Promedio (min)'},
        color='tiempo_promedio',
        color_continuous_scale='RdYlGn_r'
    )
    
    fig.update_layout(
        xaxis_title="Número de Andén",
        yaxis_title="Tiempo Promedio (minutos)",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_dashboard():
    """Renderiza la página completa del dashboard"""
    st.markdown("## Dashboard - Vista General")
    st.caption(f"Última actualización: {datetime.now().strftime('%H:%M:%S')}")
    
    # Configurar auto-refresh
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True
    
    # Control de auto-refresh
    col1, col2 = st.columns([3, 1])
    with col2:
        auto_refresh = st.checkbox(
            "Auto-refresh (5s)",
            value=st.session_state.auto_refresh,
            help="Actualizar datos automáticamente cada 5 segundos"
        )
        st.session_state.auto_refresh = auto_refresh
    
    st.markdown("---")
    
    # KPIs
    render_kpis()
    
    st.markdown("---")
    
    # Mapa de andenes
    with st.expander("🗺️ Mapa de Andenes", expanded=True):
        render_mapa_andenes()
    
    st.markdown("---")
    
    # Contenido en dos columnas
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_vehiculos_activos()
    
    with col2:
        render_grafico_tiempos()
    
    # Auto-refresh usando st.rerun con time.sleep
    if st.session_state.auto_refresh:
        time.sleep(5)
        st.rerun()
