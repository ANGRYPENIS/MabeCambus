"""
============================================================================
CamBus - Módulo de Autenticación
Centro de Distribución Mabe SLP
============================================================================
Funciones para autenticación y manejo de sesiones
"""

import bcrypt
import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Tuple
from utils.db import execute_query, execute_write


def hash_password(password: str) -> str:
    """
    Genera el hash de una contraseña usando bcrypt.
    
    Args:
        password: Contraseña en texto plano
    
    Returns:
        Hash de la contraseña
    """
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifica una contraseña contra su hash.
    
    Args:
        password: Contraseña en texto plano
        password_hash: Hash almacenado
    
    Returns:
        True si la contraseña es correcta
    """
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    except Exception:
        return False


def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[Dict]]:
    """
    Autentica un usuario contra la base de datos.
    
    Args:
        username: Nombre de usuario
        password: Contraseña
    
    Returns:
        Tuple (autenticado: bool, datos_usuario: dict o None)
    """
    # Buscar usuario en la base de datos
    query = """
        SELECT id_usuario, username, password_hash, nombre_completo, rol, activo
        FROM usuarios
        WHERE username = %s
    """
    user = execute_query(query, (username.lower().strip(),), fetch='one')
    
    if not user:
        return False, None
    
    # Verificar si el usuario está activo
    if not user.get('activo', False):
        return False, None
    
    # Verificar contraseña
    if not verify_password(password, user['password_hash']):
        return False, None
    
    # Actualizar último acceso
    update_query = "UPDATE usuarios SET ultimo_acceso = NOW() WHERE id_usuario = %s"
    execute_write(update_query, (user['id_usuario'],))
    
    # Retornar datos del usuario (sin password_hash)
    user_data = {
        'id': user['id_usuario'],
        'username': user['username'],
        'nombre': user['nombre_completo'],
        'rol': user['rol']
    }
    
    return True, user_data


def init_session_state():
    """
    Inicializa las variables de sesión si no existen.
    """
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0


def login(username: str, password: str) -> Tuple[bool, str]:
    """
    Realiza el proceso de login completo.
    
    Args:
        username: Nombre de usuario
        password: Contraseña
    
    Returns:
        Tuple (éxito: bool, mensaje: str)
    """
    init_session_state()
    
    # Verificar intentos máximos
    if st.session_state.login_attempts >= 5:
        return False, "❌ Demasiados intentos fallidos. Intente más tarde."
    
    # Validar campos
    if not username or not password:
        return False, "❌ Complete todos los campos"
    
    # Autenticar
    success, user_data = authenticate_user(username, password)
    
    if success and user_data:
        st.session_state.authenticated = True
        st.session_state.user = user_data
        st.session_state.login_attempts = 0
        return True, f"✅ Bienvenido, {user_data['nombre']}"
    else:
        st.session_state.login_attempts += 1
        intentos_restantes = 5 - st.session_state.login_attempts
        return False, f"❌ Credenciales incorrectas. Intentos restantes: {intentos_restantes}"


def logout():
    """
    Cierra la sesión del usuario.
    """
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.login_attempts = 0


def is_authenticated() -> bool:
    """
    Verifica si hay un usuario autenticado.
    
    Returns:
        True si hay sesión activa
    """
    init_session_state()
    return st.session_state.authenticated and st.session_state.user is not None


def get_current_user() -> Optional[Dict]:
    """
    Obtiene los datos del usuario actual.
    
    Returns:
        Diccionario con datos del usuario o None
    """
    if is_authenticated():
        return st.session_state.user
    return None


def get_user_role() -> Optional[str]:
    """
    Obtiene el rol del usuario actual.
    
    Returns:
        Rol del usuario o None
    """
    user = get_current_user()
    return user.get('rol') if user else None


def has_permission(required_roles: list) -> bool:
    """
    Verifica si el usuario tiene uno de los roles requeridos.
    
    Args:
        required_roles: Lista de roles permitidos
    
    Returns:
        True si el usuario tiene permiso
    """
    user_role = get_user_role()
    if not user_role:
        return False
    return user_role in required_roles


def require_auth(func):
    """
    Decorador para requerir autenticación en una página.
    """
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.warning("⚠️ Debe iniciar sesión para acceder a esta página")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_role(allowed_roles: list):
    """
    Decorador para requerir roles específicos.
    
    Args:
        allowed_roles: Lista de roles permitidos
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_authenticated():
                st.warning("⚠️ Debe iniciar sesión para acceder a esta página")
                st.stop()
            if not has_permission(allowed_roles):
                st.error("🚫 No tiene permisos para acceder a esta página")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def render_login_page():
    """
    Renderiza la página de login.
    """
    # Ocultar sidebar en la página de login
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Iniciar Sesión")
        st.markdown("---")
        
        with st.form("login_form"):
            username = st.text_input(
                "Usuario",
                placeholder="Ingrese su usuario",
                help="Usuario asignado por el administrador"
            )
            
            password = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Ingrese su contraseña"
            )
            
            col_a, col_b = st.columns(2)
            with col_b:
                submit = st.form_submit_button(
                    "Ingresar",
                    use_container_width=True,
                    type="primary"
                )
            
            if submit:
                with st.spinner("Verificando credenciales..."):
                    success, message = login(username, password)
                    
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        st.markdown("---")
        st.caption("CamBus v1.0 - Centro de Distribución Mabe SLP")
