"""
============================================================================
CamBus - Módulo de Conexión a Base de Datos
Centro de Distribución Mabe SLP
============================================================================
Funciones para conexión y operaciones con PostgreSQL
"""

import os
import yaml
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import streamlit as st
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Tuple
import pandas as pd


def load_config() -> dict:
    """Carga la configuración desde config.yaml"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@st.cache_resource
def get_connection_pool():
    """
    Crea y retorna un pool de conexiones a PostgreSQL.
    Usa st.cache_resource para mantener el pool entre recargas.
    """
    config = load_config()
    db_config = config['database']
    
    # La contraseña puede venir de variable de entorno
    password = os.getenv('DB_PASSWORD', db_config.get('password', ''))
    
    try:
        connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['name'],
            user=db_config['user'],
            password=password
        )
        return connection_pool
    except Exception as e:
        st.error(f"❌ Error al conectar con la base de datos: {str(e)}")
        return None


def get_connection():
    """Obtiene una conexión del pool"""
    pool_conn = get_connection_pool()
    if pool_conn:
        return pool_conn.getconn()
    return None


def release_connection(conn):
    """Libera una conexión de vuelta al pool"""
    pool_conn = get_connection_pool()
    if pool_conn and conn:
        pool_conn.putconn(conn)


def execute_query(query: str, params: tuple = None, fetch: str = 'all') -> Optional[List[Dict]]:
    """
    Ejecuta una consulta SELECT y retorna los resultados.
    
    Args:
        query: Consulta SQL a ejecutar
        params: Parámetros para la consulta (previene SQL injection)
        fetch: 'all' para todos los registros, 'one' para uno solo
    
    Returns:
        Lista de diccionarios con los resultados o None si hay error
    """
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return None
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            
            if fetch == 'one':
                result = cursor.fetchone()
                return dict(result) if result else None
            else:
                results = cursor.fetchall()
                return [dict(row) for row in results]
                
    except Exception as e:
        st.error(f"❌ Error en consulta: {str(e)}")
        return None
    finally:
        if conn:
            release_connection(conn)


def execute_write(query: str, params: tuple = None) -> Tuple[bool, str]:
    """
    Ejecuta una consulta INSERT, UPDATE o DELETE.
    
    Args:
        query: Consulta SQL a ejecutar
        params: Parámetros para la consulta
    
    Returns:
        Tuple (éxito: bool, mensaje: str)
    """
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return False, "No se pudo conectar a la base de datos"
        
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            return True, "Operación exitosa"
            
    except Exception as e:
        if conn:
            conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        if conn:
            release_connection(conn)


def execute_function(func_name: str, params: tuple = None) -> Tuple[bool, Any]:
    """
    Ejecuta una función almacenada de PostgreSQL.
    
    Args:
        func_name: Nombre de la función
        params: Parámetros para la función
    
    Returns:
        Tuple (éxito: bool, resultado o mensaje de error)
    """
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return False, "No se pudo conectar a la base de datos"
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Construir llamada a función
            placeholders = ', '.join(['%s'] * len(params)) if params else ''
            query = f"SELECT * FROM {func_name}({placeholders})"
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.commit()
            return True, dict(result) if result else None
            
    except Exception as e:
        if conn:
            conn.rollback()
        return False, str(e)
    finally:
        if conn:
            release_connection(conn)


# ============================================================================
# FUNCIONES ESPECÍFICAS DEL DASHBOARD
# ============================================================================

@st.cache_data(ttl=5)
def get_dashboard_stats() -> Dict[str, Any]:
    """
    Obtiene las estadísticas del dashboard en tiempo real.
    Cache de 5 segundos para auto-refresh.
    """
    stats = {
        'total_andenes': 100,
        'ocupados': 0,
        'libres': 100,
        'vehiculos_hoy': 0,
        'tiempo_promedio': 0
    }
    
    # Total de andenes activos
    result = execute_query("SELECT COUNT(*) as count FROM andenes WHERE activo = true", fetch='one')
    if result:
        stats['total_andenes'] = result.get('count', 100)
    
    # Andenes ocupados (desde vista)
    result = execute_query("SELECT COUNT(*) as count FROM vw_dashboard_tiempo_real WHERE estado_actual = 'OCUPADO'", fetch='one')
    if result:
        stats['ocupados'] = result.get('count', 0)
        stats['libres'] = stats['total_andenes'] - stats['ocupados']
    
    # Vehículos hoy (entradas)
    result = execute_query("""
        SELECT COUNT(*) as count 
        FROM registros_vehiculos 
        WHERE DATE(fecha_hora) = CURRENT_DATE AND tipo_evento = 'ENTRADA'
    """, fetch='one')
    if result:
        stats['vehiculos_hoy'] = result.get('count', 0)
    
    # Tiempo promedio de estancia (en minutos)
    result = execute_query("""
        SELECT COALESCE(AVG(duracion_segundos / 60.0), 0) as promedio
        FROM estancias_vehiculos
        WHERE DATE(hora_entrada) = CURRENT_DATE
    """, fetch='one')
    if result:
        stats['tiempo_promedio'] = round(result.get('promedio', 0), 1)
    
    return stats


@st.cache_data(ttl=5)
def get_andenes_estado() -> List[Dict]:
    """
    Obtiene el estado de todos los andenes para el mapa.
    """
    query = """
        SELECT 
            a.id_anden as id,
            a.numero_anden as numero,
            a.estado_actual as estado,
            ev.placa,
            EXTRACT(EPOCH FROM (NOW() - ev.hora_entrada))/60 as minutos
        FROM andenes a
        LEFT JOIN estancias_vehiculos ev ON a.id_anden = ev.id_anden 
            AND ev.estado = 'ACTIVA'
        WHERE a.activo = true
        ORDER BY a.numero_anden
    """
    result = execute_query(query)
    return result if result else []


@st.cache_data(ttl=5)
def get_vehiculos_activos() -> pd.DataFrame:
    """
    Obtiene los vehículos actualmente en andenes.
    """
    query = """
        SELECT 
            a.numero_anden as anden,
            ev.placa,
            ev.hora_entrada,
            EXTRACT(EPOCH FROM (NOW() - ev.hora_entrada))/60 as minutos,
            a.tipo_operacion,
            ev.id_estancia as registro_id
        FROM estancias_vehiculos ev
        INNER JOIN andenes a ON ev.id_anden = a.id_anden
        WHERE ev.estado = 'ACTIVA'
        ORDER BY ev.hora_entrada DESC
    """
    result = execute_query(query)
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()


@st.cache_data(ttl=60)
def get_top_andenes_tiempo() -> pd.DataFrame:
    """
    Obtiene el top 10 de andenes con mayor tiempo promedio.
    """
    query = """
        SELECT 
            a.numero_anden as anden,
            COALESCE(AVG(ev.duracion_segundos / 60.0), 0) as tiempo_promedio
        FROM andenes a
        LEFT JOIN estancias_vehiculos ev ON a.id_anden = ev.id_anden
        WHERE a.activo = true
        GROUP BY a.numero_anden
        ORDER BY tiempo_promedio DESC
        LIMIT 10
    """
    result = execute_query(query)
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()


# ============================================================================
# FUNCIONES DE REGISTRO DE VEHÍCULOS
# ============================================================================

def get_andenes_libres() -> List[Dict]:
    """Obtiene lista de andenes disponibles (libres)"""
    query = """
        SELECT id_anden as id, numero_anden as numero
        FROM andenes
        WHERE estado_actual = 'LIBRE' AND activo = true
        ORDER BY numero_anden
    """
    result = execute_query(query)
    return result if result else []


def get_andenes_ocupados() -> List[Dict]:
    """Obtiene lista de andenes ocupados con información del vehículo"""
    query = """
        SELECT 
            a.id_anden as id,
            a.numero_anden as numero,
            ev.placa,
            ev.id_estancia as registro_id
        FROM andenes a
        INNER JOIN estancias_vehiculos ev ON a.id_anden = ev.id_anden
        WHERE a.estado_actual = 'OCUPADO' AND ev.estado = 'ACTIVA'
        ORDER BY a.numero_anden
    """
    result = execute_query(query)
    return result if result else []


def get_camaras_anden(anden_id: int) -> List[Dict]:
    """Obtiene cámaras activas de un andén específico"""
    query = """
        SELECT id_camara as id, nombre, ip_address as ubicacion
        FROM camaras
        WHERE id_anden = %s AND estado = 'ACTIVA'
        ORDER BY nombre
    """
    result = execute_query(query, (anden_id,))
    return result if result else []


def registrar_entrada_vehiculo(
    placa: str,
    anden_id: int,
    camara_id: int,
    tipo_vehiculo: str,
    transportista: str,
    confianza_ocr: float,
    observaciones: str,
    usuario_id: int
) -> Tuple[bool, str]:
    """
    Registra la entrada de un vehículo al andén.
    Llama a la función almacenada registrar_entrada_vehiculo.
    """
    try:
        success, result = execute_function(
            'registrar_entrada_vehiculo',
            (placa, anden_id, camara_id, tipo_vehiculo, transportista, 
             confianza_ocr, observaciones, usuario_id)
        )
        
        if success:
            return True, f"✅ Entrada registrada correctamente para {placa}"
        else:
            return False, f"❌ Error: {result}"
    except Exception as e:
        return False, f"❌ Error al registrar entrada: {str(e)}"


def registrar_salida_vehiculo(registro_id: int, usuario_id: int) -> Tuple[bool, str, Optional[float]]:
    """
    Registra la salida de un vehículo del andén.
    Llama a la función almacenada registrar_salida_vehiculo.
    
    Returns:
        Tuple (éxito, mensaje, duración en minutos)
    """
    try:
        success, result = execute_function(
            'registrar_salida_vehiculo',
            (registro_id, usuario_id)
        )
        
        if success and result:
            duracion = result.get('duracion_minutos', 0)
            return True, f"✅ Salida registrada. Duración: {duracion:.1f} minutos", duracion
        else:
            return False, f"❌ Error: {result}", None
    except Exception as e:
        return False, f"❌ Error al registrar salida: {str(e)}", None


# ============================================================================
# FUNCIONES DE REPORTES
# ============================================================================

@st.cache_data(ttl=300)
def get_flujo_horario(fecha_inicio: date, fecha_fin: date) -> pd.DataFrame:
    """Obtiene reporte de flujo por hora"""
    # Consulta directa en lugar de vista que puede no existir
    query = """
        SELECT 
            DATE(fecha_hora) as fecha,
            EXTRACT(HOUR FROM fecha_hora)::int as hora,
            COUNT(*) as total_vehiculos,
            COUNT(CASE WHEN tipo_evento = 'ENTRADA' THEN 1 END) as entradas,
            COUNT(CASE WHEN tipo_evento = 'SALIDA' THEN 1 END) as salidas
        FROM registros_vehiculos
        WHERE DATE(fecha_hora) BETWEEN %s AND %s
        GROUP BY DATE(fecha_hora), EXTRACT(HOUR FROM fecha_hora)
        ORDER BY fecha, hora
    """
    result = execute_query(query, (fecha_inicio, fecha_fin))
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()


@st.cache_data(ttl=300)
def get_eficiencia_andenes(fecha_inicio: date, fecha_fin: date) -> pd.DataFrame:
    """Obtiene reporte de eficiencia de andenes"""
    # Consulta directa en lugar de vista que puede no existir
    query = """
        SELECT 
            a.numero_anden as anden,
            COUNT(ev.id_estancia) as total_operaciones,
            AVG(COALESCE(ev.duracion_segundos / 60.0, 0)) as promedio_minutos,
            SUM(COALESCE(ev.duracion_segundos / 60.0, 0)) as tiempo_total_minutos,
            ROUND(COUNT(ev.id_estancia)::numeric / GREATEST(EXTRACT(DAY FROM (%s::date - %s::date + 1)), 1), 2) as operaciones_por_dia
        FROM andenes a
        LEFT JOIN estancias_vehiculos ev ON a.id_anden = ev.id_anden 
            AND DATE(ev.hora_entrada) BETWEEN %s AND %s
        GROUP BY a.id_anden, a.numero_anden
        ORDER BY total_operaciones DESC
    """
    result = execute_query(query, (fecha_fin, fecha_inicio, fecha_inicio, fecha_fin))
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()


@st.cache_data(ttl=300)
def get_tiempos_permanencia(fecha_inicio: date, fecha_fin: date) -> pd.DataFrame:
    """Obtiene reporte de tiempos de permanencia"""
    query = """
        SELECT 
            a.numero_anden as anden,
            ev.placa,
            rv.tipo_vehiculo,
            ev.hora_entrada as fecha_hora_entrada,
            ev.hora_salida as fecha_hora_salida,
            COALESCE(ev.duracion_segundos / 60.0, 
                     EXTRACT(EPOCH FROM (COALESCE(ev.hora_salida, NOW()) - ev.hora_entrada))/60) as duracion_minutos
        FROM estancias_vehiculos ev
        INNER JOIN andenes a ON ev.id_anden = a.id_anden
        LEFT JOIN registros_vehiculos rv ON ev.id_registro_entrada = rv.id_registro
        WHERE DATE(ev.hora_entrada) BETWEEN %s AND %s
        ORDER BY ev.hora_entrada DESC
    """
    result = execute_query(query, (fecha_inicio, fecha_fin))
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()


@st.cache_data(ttl=300)
def get_productos_mas_movidos(fecha_inicio: date, fecha_fin: date) -> pd.DataFrame:
    """Obtiene reporte de productos más movidos"""
    # Consulta directa - asumiendo que hay una tabla de productos relacionada con vehículos
    # Si no existe tal relación, devolvemos un DataFrame vacío con mensaje
    query = """
        SELECT 
            COALESCE(rv.tipo_vehiculo, 'Sin especificar') as producto,
            COUNT(*) as cantidad,
            DATE(rv.fecha_hora) as fecha
        FROM registros_vehiculos rv
        WHERE DATE(rv.fecha_hora) BETWEEN %s AND %s
        GROUP BY rv.tipo_vehiculo, DATE(rv.fecha_hora)
        ORDER BY cantidad DESC
        LIMIT 20
    """
    result = execute_query(query, (fecha_inicio, fecha_fin))
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()


# ============================================================================
# FUNCIONES DE ADMINISTRACIÓN
# ============================================================================

def get_usuarios() -> List[Dict]:
    """Obtiene lista de todos los usuarios"""
    query = """
        SELECT id_usuario, username, nombre_completo, email, rol, activo, ultimo_acceso, created_at
        FROM usuarios
        ORDER BY username
    """
    return execute_query(query) or []


def crear_usuario(username: str, password_hash: str, nombre: str, email: str, rol: str) -> Tuple[bool, str]:
    """Crea un nuevo usuario"""
    query = """
        INSERT INTO usuarios (username, password_hash, nombre_completo, email, rol, activo)
        VALUES (%s, %s, %s, %s, %s, true)
    """
    return execute_write(query, (username, password_hash, nombre, email, rol))


def actualizar_estado_usuario(usuario_id: int, activo: bool) -> Tuple[bool, str]:
    """Activa o desactiva un usuario"""
    query = "UPDATE usuarios SET activo = %s WHERE id_usuario = %s"
    return execute_write(query, (activo, usuario_id))


def get_todos_andenes() -> List[Dict]:
    """Obtiene todos los andenes con su estado"""
    query = """
        SELECT id_anden as id, numero_anden as numero, estado_actual as estado, zona as ubicacion, tipo_operacion, activo
        FROM andenes
        ORDER BY numero_anden
    """
    return execute_query(query) or []


def actualizar_estado_anden(anden_id: int, estado: str) -> Tuple[bool, str]:
    """Actualiza el estado de un andén"""
    query = "UPDATE andenes SET estado_actual = %s, ultimo_cambio_estado = NOW() WHERE id_anden = %s"
    return execute_write(query, (estado, anden_id))


def get_camaras() -> List[Dict]:
    """Obtiene todas las cámaras"""
    query = """
        SELECT c.id_camara as id, c.nombre, c.ip_address as ubicacion, c.url_stream, 
               CASE WHEN c.estado = 'ACTIVA' THEN true ELSE false END as activa,
               a.numero_anden as anden_numero
        FROM camaras c
        LEFT JOIN andenes a ON c.id_anden = a.id_anden
        ORDER BY c.nombre
    """
    return execute_query(query) or []


def crear_camara(nombre: str, ip_address: str, url: str, anden_id: int) -> Tuple[bool, str]:
    """Crea una nueva cámara"""
    query = """
        INSERT INTO camaras (nombre, ip_address, url_stream, id_anden, estado)
        VALUES (%s, %s::inet, %s, %s, 'ACTIVA')
    """
    return execute_write(query, (nombre, ip_address, url, anden_id))


def actualizar_camara(camara_id: int, activa: bool) -> Tuple[bool, str]:
    """Activa o desactiva una cámara"""
    estado = 'ACTIVA' if activa else 'INACTIVA'
    query = "UPDATE camaras SET estado = %s WHERE id_camara = %s"
    return execute_write(query, (estado, camara_id))


def eliminar_camara(camara_id: int) -> Tuple[bool, str]:
    """Elimina una cámara"""
    query = "DELETE FROM camaras WHERE id_camara = %s"
    return execute_write(query, (camara_id,))


def test_connection() -> bool:
    """Prueba la conexión a la base de datos"""
    result = execute_query("SELECT 1 as test", fetch='one')
    return result is not None
