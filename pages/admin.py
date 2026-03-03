"""
============================================================================
CamBus - Página de Administración
Centro de Distribución Mabe SLP
============================================================================
Gestión de usuarios, andenes, cámaras y backups
"""

import streamlit as st
import pandas as pd
import subprocess
from datetime import datetime

from utils.db import (
    get_usuarios,
    crear_usuario,
    actualizar_estado_usuario,
    get_todos_andenes,
    actualizar_estado_anden,
    get_camaras,
    crear_camara,
    actualizar_camara,
    eliminar_camara,
    load_config
)
from utils.auth import hash_password, has_permission


# Estados de andenes
ESTADOS_ANDEN = ['LIBRE', 'OCUPADO', 'MANTENIMIENTO', 'BLOQUEADO']

# Roles de usuario
ROLES_USUARIO = ['ADMIN', 'SUPERVISOR', 'OPERADOR']


def render_gestion_usuarios():
    """Renderiza la sección de gestión de usuarios"""
    st.markdown("### Gestión de Usuarios")
    
    # Obtener usuarios
    usuarios = get_usuarios()
    
    if usuarios:
        # Mostrar tabla de usuarios
        df_usuarios = pd.DataFrame(usuarios)
        
        # Formatear columnas
        if 'ultimo_acceso' in df_usuarios.columns:
            df_usuarios['ultimo_acceso'] = pd.to_datetime(df_usuarios['ultimo_acceso']).dt.strftime('%Y-%m-%d %H:%M')
        if 'created_at' in df_usuarios.columns:
            df_usuarios['created_at'] = pd.to_datetime(df_usuarios['created_at']).dt.strftime('%Y-%m-%d')
        
        # Mostrar estado con iconos
        df_usuarios['estado'] = df_usuarios['activo'].apply(
            lambda x: '✅ Activo' if x else '❌ Inactivo'
        )
        
        # Seleccionar columnas a mostrar
        columnas_mostrar = ['id_usuario', 'username', 'nombre_completo', 'email', 'rol', 'estado', 'ultimo_acceso']
        columnas_disponibles = [c for c in columnas_mostrar if c in df_usuarios.columns]
        
        st.dataframe(
            df_usuarios[columnas_disponibles],
            use_container_width=True,
            hide_index=True
        )
        
        # Acciones sobre usuarios
        st.markdown("#### Acciones")
        col1, col2 = st.columns(2)
        
        with col1:
            usuario_seleccionado = st.selectbox(
                "Seleccionar Usuario",
                options=[f"{u['id_usuario']} - {u['username']}" for u in usuarios],
                help="Seleccione el usuario a modificar"
            )
        
        with col2:
            if usuario_seleccionado:
                usuario_id = int(usuario_seleccionado.split(' - ')[0])
                usuario_actual = next((u for u in usuarios if u['id_usuario'] == usuario_id), None)
                
                if usuario_actual:
                    if usuario_actual['activo']:
                        if st.button("Desactivar Usuario", type="secondary"):
                            success, msg = actualizar_estado_usuario(usuario_id, False)
                            if success:
                                st.success("Usuario desactivado correctamente")
                                st.rerun()
                            else:
                                st.error(msg)
                    else:
                        if st.button("Activar Usuario", type="primary"):
                            success, msg = actualizar_estado_usuario(usuario_id, True)
                            if success:
                                st.success("Usuario activado correctamente")
                                st.rerun()
                            else:
                                st.error(msg)
    else:
        st.info("No hay usuarios registrados")
    
    st.markdown("---")
    
    # Formulario para crear nuevo usuario
    st.markdown("#### Crear Nuevo Usuario")
    
    with st.form("form_nuevo_usuario", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nuevo_username = st.text_input(
                "Nombre de Usuario *",
                placeholder="usuario123",
                help="Nombre único para iniciar sesión"
            ).lower().strip()
            
            nuevo_password = st.text_input(
                "Contraseña *",
                type="password",
                help="Mínimo 8 caracteres"
            )
            
            nuevo_email = st.text_input(
                "Email *",
                placeholder="usuario@mabe.com.mx",
                help="Correo electrónico del usuario"
            ).lower().strip()
        
        with col2:
            nuevo_nombre = st.text_input(
                "Nombre Completo *",
                placeholder="Juan Pérez García",
                help="Nombre real del usuario"
            )
            
            nuevo_rol = st.selectbox(
                "Rol *",
                options=ROLES_USUARIO,
                help="Nivel de acceso del usuario"
            )
        
        submitted = st.form_submit_button("Crear Usuario", type="primary")
        
        if submitted:
            # Validaciones
            if not nuevo_username or not nuevo_password or not nuevo_nombre or not nuevo_email:
                st.error("❌ Complete todos los campos obligatorios")
            elif len(nuevo_password) < 8:
                st.error("❌ La contraseña debe tener al menos 8 caracteres")
            elif len(nuevo_username) < 3:
                st.error("❌ El nombre de usuario debe tener al menos 3 caracteres")
            elif '@' not in nuevo_email:
                st.error("❌ Ingrese un email válido")
            else:
                # Hash de la contraseña
                password_hash = hash_password(nuevo_password)
                
                # Crear usuario
                success, msg = crear_usuario(
                    username=nuevo_username,
                    password_hash=password_hash,
                    nombre=nuevo_nombre,
                    email=nuevo_email,
                    rol=nuevo_rol
                )
                
                if success:
                    st.success(f"✅ Usuario '{nuevo_username}' creado correctamente")
                    st.rerun()
                else:
                    st.error(f"❌ Error al crear usuario: {msg}")


def render_gestion_andenes():
    """Renderiza la sección de gestión de andenes"""
    st.markdown("### Gestión de Andenes")
    
    # Obtener andenes
    andenes = get_todos_andenes()
    
    if andenes:
        # Estadísticas
        total = len(andenes)
        por_estado = {}
        for a in andenes:
            estado = a.get('estado', 'DESCONOCIDO')
            por_estado[estado] = por_estado.get(estado, 0) + 1
        
        cols = st.columns(len(por_estado) + 1)
        cols[0].metric("Total Andenes", total)
        for i, (estado, cantidad) in enumerate(por_estado.items()):
            cols[i + 1].metric(estado, cantidad)
        
        st.markdown("---")
        
        # Tabla de andenes
        df_andenes = pd.DataFrame(andenes)
        
        # Añadir iconos de estado
        estado_iconos = {
            'LIBRE': '🟢',
            'OCUPADO': '🔴',
            'MANTENIMIENTO': '🟡',
            'BLOQUEADO': '⚫'
        }
        df_andenes['estado_visual'] = df_andenes['estado'].apply(
            lambda x: f"{estado_iconos.get(x, '⚪')} {x}"
        )
        
        # Seleccionar solo columnas que existen en el DataFrame
        columnas_disponibles = ['numero', 'estado_visual']
        if 'ubicacion' in df_andenes.columns:
            columnas_disponibles.append('ubicacion')
        if 'tipo_operacion' in df_andenes.columns:
            columnas_disponibles.append('tipo_operacion')
        
        st.dataframe(
            df_andenes[columnas_disponibles],
            use_container_width=True,
            hide_index=True
        )
        
        # Cambiar estado de andén
        st.markdown("#### Cambiar Estado de Andén")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            andenes_opciones = {f"Andén {a['numero']}": a['id'] for a in andenes}
            anden_seleccionado = st.selectbox(
                "Seleccionar Andén",
                options=list(andenes_opciones.keys())
            )
        
        with col2:
            nuevo_estado = st.selectbox(
                "Nuevo Estado",
                options=ESTADOS_ANDEN
            )
        
        with col3:
            st.write("")  # Espaciador
            st.write("")
            if st.button("Cambiar Estado", type="primary"):
                if anden_seleccionado:
                    anden_id = andenes_opciones[anden_seleccionado]
                    success, msg = actualizar_estado_anden(anden_id, nuevo_estado)
                    
                    if success:
                        st.success(f"✅ Estado de {anden_seleccionado} cambiado a {nuevo_estado}")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {msg}")
    else:
        st.warning("No se pudieron cargar los andenes")


def render_gestion_camaras():
    """Renderiza la sección de gestión de cámaras"""
    st.markdown("### Gestión de Cámaras")
    
    # Obtener cámaras
    camaras = get_camaras()
    
    if camaras:
        df_camaras = pd.DataFrame(camaras)
        
        # Estado con iconos
        df_camaras['estado_visual'] = df_camaras['activa'].apply(
            lambda x: '🟢 Activa' if x else '🔴 Inactiva'
        )
        
        # Seleccionar solo columnas que existen en el DataFrame
        columnas_camaras = ['id', 'nombre']
        if 'ubicacion' in df_camaras.columns:
            columnas_camaras.append('ubicacion')
        if 'anden_numero' in df_camaras.columns:
            columnas_camaras.append('anden_numero')
        columnas_camaras.append('estado_visual')
        
        st.dataframe(
            df_camaras[columnas_camaras],
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        
        # Acciones sobre cámaras
        st.markdown("#### Acciones")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            camara_seleccionada = st.selectbox(
                "Seleccionar Cámara",
                options=[f"{c['id']} - {c['nombre']}" for c in camaras]
            )
        
        with col2:
            if camara_seleccionada:
                camara_id = int(camara_seleccionada.split(' - ')[0])
                camara_actual = next((c for c in camaras if c['id'] == camara_id), None)
                
                if camara_actual:
                    if camara_actual['activa']:
                        if st.button("🔴 Desactivar"):
                            success, msg = actualizar_camara(camara_id, False)
                            if success:
                                st.success("Cámara desactivada")
                                st.rerun()
                            else:
                                st.error(msg)
                    else:
                        if st.button("🟢 Activar"):
                            success, msg = actualizar_camara(camara_id, True)
                            if success:
                                st.success("Cámara activada")
                                st.rerun()
                            else:
                                st.error(msg)
        
        with col3:
            if camara_seleccionada:
                if st.button("Eliminar", type="secondary"):
                    camara_id = int(camara_seleccionada.split(' - ')[0])
                    success, msg = eliminar_camara(camara_id)
                    if success:
                        st.success("Cámara eliminada")
                        st.rerun()
                    else:
                        st.error(msg)
    else:
        st.info("No hay cámaras registradas")
    
    st.markdown("---")
    
    # Formulario para crear nueva cámara
    st.markdown("#### Agregar Nueva Cámara")
    
    # Obtener andenes para el selector
    andenes = get_todos_andenes()
    
    with st.form("form_nueva_camara", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            cam_nombre = st.text_input(
                "Nombre de la Cámara *",
                placeholder="CAM-ANDEN-01"
            )
            
            cam_ip = st.text_input(
                "Dirección IP *",
                placeholder="192.168.1.100"
            )
        
        with col2:
            cam_url = st.text_input(
                "URL del Stream",
                placeholder="rtsp://192.168.1.100:554/stream"
            )
            
            if andenes:
                andenes_opciones = {f"Andén {a['numero']}": a['id'] for a in andenes}
                cam_anden = st.selectbox(
                    "Andén Asociado *",
                    options=list(andenes_opciones.keys())
                )
            else:
                cam_anden = None
                st.warning("No hay andenes disponibles")
        
        submitted = st.form_submit_button("Agregar Cámara", type="primary")
        
        if submitted:
            if not cam_nombre or not cam_ip or not cam_anden:
                st.error("❌ Complete los campos obligatorios")
            else:
                anden_id = andenes_opciones.get(cam_anden)
                success, msg = crear_camara(
                    nombre=cam_nombre,
                    ip_address=cam_ip,
                    url=cam_url or "",
                    anden_id=anden_id
                )
                
                if success:
                    st.success(f"✅ Cámara '{cam_nombre}' agregada correctamente")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {msg}")


def render_backup():
    """Renderiza la sección de backup"""
    st.markdown("### 💾 Backup de Base de Datos")
    
    st.info("""
    ℹ️ El backup genera un archivo SQL con toda la estructura y datos de la base de datos.
    Este archivo puede usarse para restaurar el sistema en caso de pérdida de datos.
    """)
    
    config = load_config()
    db_config = config.get('database', {})
    
    # Mostrar configuración actual
    st.markdown("#### Configuración Actual")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(f"Host: {db_config.get('host', 'localhost')}")
    with col2:
        st.text(f"Puerto: {db_config.get('port', 5432)}")
    with col3:
        st.text(f"Base de datos: {db_config.get('name', 'cambus_db')}")
    
    st.markdown("---")
    
    # Botón de backup
    if st.button("🔄 Generar Backup", type="primary", use_container_width=True):
        with st.spinner("Generando backup... Esto puede tomar unos minutos."):
            try:
                # Generar nombre de archivo con timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"backup_cambus_{timestamp}.sql"
                
                # Comando pg_dump
                cmd = [
                    "pg_dump",
                    "-h", db_config.get('host', 'localhost'),
                    "-p", str(db_config.get('port', 5432)),
                    "-U", db_config.get('user', 'postgres'),
                    "-d", db_config.get('name', 'cambus_db'),
                    "-f", backup_filename
                ]
                
                # Ejecutar pg_dump
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    st.success(f"✅ Backup generado correctamente: {backup_filename}")
                    
                    # Ofrecer descarga si el archivo existe
                    try:
                        with open(backup_filename, 'r') as f:
                            backup_content = f.read()
                        
                        st.download_button(
                            label="📥 Descargar Backup",
                            data=backup_content,
                            file_name=backup_filename,
                            mime="application/sql"
                        )
                    except Exception as e:
                        st.warning(f"El backup se guardó en: {backup_filename}")
                else:
                    st.error(f"❌ Error al generar backup: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                st.error("❌ El backup tardó demasiado tiempo. Intente de nuevo.")
            except FileNotFoundError:
                st.error("❌ pg_dump no está instalado o no está en el PATH")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    
    # Información adicional
    with st.expander("ℹ️ Instrucciones de Restauración"):
        st.markdown("""
        Para restaurar un backup, ejecute el siguiente comando en terminal:
        
        ```bash
        psql -h localhost -U postgres -d cambus_db < backup_cambus_YYYYMMDD_HHMMSS.sql
        ```
        
        **Nota:** Asegúrese de que la base de datos `cambus_db` exista antes de restaurar.
        """)


def render_admin():
    """Renderiza la página completa de administración"""
    st.markdown("## Administración del Sistema")
    st.caption("Gestión de usuarios, andenes, cámaras y backups")
    
    st.markdown("---")
    
    # Crear pestañas para cada sección
    tab1, tab2, tab3, tab4 = st.tabs([
        "Usuarios",
        "Andenes",
        "Cámaras",
        "Backup"
    ])
    
    with tab1:
        render_gestion_usuarios()
    
    with tab2:
        render_gestion_andenes()
    
    with tab3:
        render_gestion_camaras()
    
    with tab4:
        render_backup()
