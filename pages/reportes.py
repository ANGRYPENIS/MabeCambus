"""
============================================================================
CamBus - Página de Reportes y Análisis
Centro de Distribución Mabe SLP
============================================================================
Generación de reportes y visualización de datos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from io import BytesIO

from utils.db import (
    get_flujo_horario,
    get_eficiencia_andenes,
    get_tiempos_permanencia,
    get_productos_mas_movidos
)


# Tipos de reportes disponibles
TIPOS_REPORTE = {
    'flujo_horario': {
        'nombre': 'Flujo por Hora',
        'descripcion': 'Análisis del flujo de vehículos por hora del día'
    },
    'eficiencia_andenes': {
        'nombre': 'Eficiencia de Andenes',
        'descripcion': 'Métricas de eficiencia por andén'
    },
    'tiempos_permanencia': {
        'nombre': 'Tiempos de Permanencia',
        'descripcion': 'Análisis de tiempos de estancia de vehículos'
    },
    'productos_movidos': {
        'nombre': 'Productos Más Movidos',
        'descripcion': 'Ranking de productos con mayor movimiento'
    }
}


def exportar_csv(df: pd.DataFrame, nombre: str) -> bytes:
    """
    Convierte un DataFrame a CSV para descarga.
    
    Args:
        df: DataFrame a exportar
        nombre: Nombre del archivo
    
    Returns:
        Bytes del archivo CSV
    """
    return df.to_csv(index=False).encode('utf-8')


def exportar_excel(df: pd.DataFrame, nombre: str) -> bytes:
    """
    Convierte un DataFrame a Excel para descarga.
    
    Args:
        df: DataFrame a exportar
        nombre: Nombre del archivo
    
    Returns:
        Bytes del archivo Excel
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reporte')
    return output.getvalue()


def render_reporte_flujo_horario(fecha_inicio: date, fecha_fin: date):
    """Renderiza el reporte de flujo por hora"""
    st.markdown("### Reporte de Flujo por Hora")
    
    with st.spinner("Generando reporte..."):
        df = get_flujo_horario(fecha_inicio, fecha_fin)
    
    if df.empty:
        st.warning("No hay datos para el período seleccionado")
        return None
    
    # Mostrar resumen
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Entradas", int(df['entradas'].sum()) if 'entradas' in df.columns else 0)
    with col2:
        st.metric("Total Salidas", int(df['salidas'].sum()) if 'salidas' in df.columns else 0)
    with col3:
        st.metric("Días Analizados", len(df['fecha'].unique()) if 'fecha' in df.columns else 0)
    
    st.markdown("---")
    
    # Gráfico de líneas por hora
    if 'hora' in df.columns and 'entradas' in df.columns:
        # Agrupar por hora
        df_hora = df.groupby('hora').agg({
            'entradas': 'sum',
            'salidas': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_hora['hora'],
            y=df_hora['entradas'],
            mode='lines+markers',
            name='Entradas',
            line=dict(color='#28a745', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df_hora['hora'],
            y=df_hora['salidas'],
            mode='lines+markers',
            name='Salidas',
            line=dict(color='#dc3545', width=3)
        ))
        
        fig.update_layout(
            title='Flujo de Vehículos por Hora',
            xaxis_title='Hora del Día',
            yaxis_title='Cantidad de Vehículos',
            legend_title='Tipo',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de datos
    with st.expander("Ver Datos Detallados", expanded=False):
        st.dataframe(df, use_container_width=True)
    
    return df


def render_reporte_eficiencia(fecha_inicio: date, fecha_fin: date):
    """Renderiza el reporte de eficiencia de andenes"""
    st.markdown("### ⚡ Reporte de Eficiencia de Andenes")
    
    with st.spinner("Generando reporte..."):
        df = get_eficiencia_andenes(fecha_inicio, fecha_fin)
    
    if df.empty:
        st.warning("No hay datos para el período seleccionado")
        return None
    
    # Mostrar resumen
    col1, col2, col3 = st.columns(3)
    with col1:
        eficiencia_promedio = df['eficiencia'].mean() if 'eficiencia' in df.columns else 0
        st.metric("Eficiencia Promedio", f"{eficiencia_promedio:.1f}%")
    with col2:
        if 'eficiencia' in df.columns:
            mejor_anden = df.loc[df['eficiencia'].idxmax()]['anden'] if not df.empty else 'N/A'
            st.metric("Mejor Andén", mejor_anden)
    with col3:
        andenes_analizados = len(df)
        st.metric("Andenes Analizados", andenes_analizados)
    
    st.markdown("---")
    
    # Gráfico de barras de eficiencia
    if 'anden' in df.columns and 'eficiencia' in df.columns:
        fig = px.bar(
            df.head(20),
            x='anden',
            y='eficiencia',
            color='eficiencia',
            color_continuous_scale='RdYlGn',
            title='Eficiencia por Andén (Top 20)'
        )
        
        fig.update_layout(
            xaxis_title='Andén',
            yaxis_title='Eficiencia (%)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de datos
    with st.expander("Ver Datos Detallados", expanded=False):
        st.dataframe(df, use_container_width=True)
    
    return df


def render_reporte_permanencia(fecha_inicio: date, fecha_fin: date):
    """Renderiza el reporte de tiempos de permanencia"""
    st.markdown("### ⏱️ Reporte de Tiempos de Permanencia")
    
    with st.spinner("Generando reporte..."):
        df = get_tiempos_permanencia(fecha_inicio, fecha_fin)
    
    if df.empty:
        st.warning("No hay datos para el período seleccionado")
        return None
    
    # Calcular estadísticas
    if 'duracion_minutos' in df.columns:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tiempo Promedio", f"{df['duracion_minutos'].mean():.1f} min")
        with col2:
            st.metric("Tiempo Máximo", f"{df['duracion_minutos'].max():.1f} min")
        with col3:
            st.metric("Tiempo Mínimo", f"{df['duracion_minutos'].min():.1f} min")
        with col4:
            st.metric("Total Vehículos", len(df))
    
    st.markdown("---")
    
    # Histograma de tiempos
    if 'duracion_minutos' in df.columns:
        fig = px.histogram(
            df,
            x='duracion_minutos',
            nbins=30,
            title='Distribución de Tiempos de Permanencia',
            labels={'duracion_minutos': 'Duración (minutos)'}
        )
        
        fig.update_layout(
            xaxis_title='Duración (minutos)',
            yaxis_title='Frecuencia',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de caja por tipo de vehículo
    if 'tipo_vehiculo' in df.columns and 'duracion_minutos' in df.columns:
        fig = px.box(
            df,
            x='tipo_vehiculo',
            y='duracion_minutos',
            title='Tiempos por Tipo de Vehículo',
            color='tipo_vehiculo'
        )
        
        fig.update_layout(
            xaxis_title='Tipo de Vehículo',
            yaxis_title='Duración (minutos)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de datos
    with st.expander("Ver Datos Detallados", expanded=False):
        # Formatear fechas para mejor visualización
        df_display = df.copy()
        if 'fecha_hora_entrada' in df_display.columns:
            df_display['fecha_hora_entrada'] = pd.to_datetime(df_display['fecha_hora_entrada']).dt.strftime('%Y-%m-%d %H:%M')
        if 'fecha_hora_salida' in df_display.columns:
            df_display['fecha_hora_salida'] = pd.to_datetime(df_display['fecha_hora_salida']).dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(df_display, use_container_width=True)
    
    return df


def render_reporte_productos(fecha_inicio: date, fecha_fin: date):
    """Renderiza el reporte de productos más movidos"""
    st.markdown("### 📦 Reporte de Productos Más Movidos")
    
    with st.spinner("Generando reporte..."):
        df = get_productos_mas_movidos(fecha_inicio, fecha_fin)
    
    if df.empty:
        st.warning("No hay datos para el período seleccionado")
        return None
    
    # Mostrar resumen
    col1, col2 = st.columns(2)
    with col1:
        total_productos = len(df)
        st.metric("Total Productos", total_productos)
    with col2:
        if 'cantidad' in df.columns:
            total_movimientos = df['cantidad'].sum()
            st.metric("Total Movimientos", int(total_movimientos))
    
    st.markdown("---")
    
    # Gráfico de barras horizontal
    if 'producto' in df.columns and 'cantidad' in df.columns:
        fig = px.bar(
            df.head(20),
            y='producto',
            x='cantidad',
            orientation='h',
            title='Top 20 Productos Más Movidos',
            color='cantidad',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            yaxis_title='Producto',
            xaxis_title='Cantidad',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de pie (top 10)
    if 'producto' in df.columns and 'cantidad' in df.columns:
        fig = px.pie(
            df.head(10),
            values='cantidad',
            names='producto',
            title='Distribución Top 10 Productos'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de datos
    with st.expander("Ver Datos Detallados", expanded=False):
        st.dataframe(df, use_container_width=True)
    
    return df


def render_reportes():
    """Renderiza la página completa de reportes"""
    st.markdown("## Reportes y Análisis")
    st.caption("Genere reportes detallados del sistema")
    
    st.markdown("---")
    
    # Controles de configuración
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        tipo_reporte = st.selectbox(
            "Tipo de Reporte",
            options=list(TIPOS_REPORTE.keys()),
            format_func=lambda x: TIPOS_REPORTE[x]['nombre'],
            help="Seleccione el tipo de reporte a generar"
        )
        st.caption(TIPOS_REPORTE[tipo_reporte]['descripcion'])
    
    with col2:
        fecha_inicio = st.date_input(
            "📅 Fecha Inicio",
            value=date.today() - timedelta(days=30),
            help="Fecha de inicio del período"
        )
    
    with col3:
        fecha_fin = st.date_input(
            "📅 Fecha Fin",
            value=date.today(),
            help="Fecha de fin del período"
        )
    
    # Validar fechas
    if fecha_inicio > fecha_fin:
        st.error("❌ La fecha de inicio debe ser anterior a la fecha de fin")
        return
    
    st.markdown("---")
    
    # Generar reporte según tipo seleccionado
    df_resultado = None
    
    if tipo_reporte == 'flujo_horario':
        df_resultado = render_reporte_flujo_horario(fecha_inicio, fecha_fin)
    elif tipo_reporte == 'eficiencia_andenes':
        df_resultado = render_reporte_eficiencia(fecha_inicio, fecha_fin)
    elif tipo_reporte == 'tiempos_permanencia':
        df_resultado = render_reporte_permanencia(fecha_inicio, fecha_fin)
    elif tipo_reporte == 'productos_movidos':
        df_resultado = render_reporte_productos(fecha_inicio, fecha_fin)
    
    # Opciones de exportación
    if df_resultado is not None and not df_resultado.empty:
        st.markdown("---")
        st.markdown("### 📥 Exportar Datos")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        nombre_archivo = f"reporte_{tipo_reporte}_{fecha_inicio}_{fecha_fin}"
        
        with col1:
            csv_data = exportar_csv(df_resultado, nombre_archivo)
            st.download_button(
                label="📄 Descargar CSV",
                data=csv_data,
                file_name=f"{nombre_archivo}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            excel_data = exportar_excel(df_resultado, nombre_archivo)
            st.download_button(
                label="Descargar Excel",
                data=excel_data,
                file_name=f"{nombre_archivo}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
