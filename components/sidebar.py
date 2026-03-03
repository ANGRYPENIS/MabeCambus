"""
============================================================================
CamBus - Componente de Navegación (Sidebar)
Centro de Distribución Mabe SLP
============================================================================
Barra lateral de navegación según rol del usuario
"""

import streamlit as st
from utils.auth import get_current_user, get_user_role, logout, has_permission


# Definición de páginas por rol
MENU_ITEMS = {
    'ADMIN': [
        {'name': 'Dashboard', 'icon': '📊', 'key': 'dashboard'},
        {'name': 'Registro Manual', 'icon': '📝', 'key': 'registro'},
        {'name': 'Reportes', 'icon': '📈', 'key': 'reportes'},
        {'name': 'Administración', 'icon': '⚙️', 'key': 'admin'},
    ],
    'SUPERVISOR': [
        {'name': 'Dashboard', 'icon': '📊', 'key': 'dashboard'},
        {'name': 'Registro Manual', 'icon': '📝', 'key': 'registro'},
        {'name': 'Reportes', 'icon': '📈', 'key': 'reportes'},
    ],
    'OPERADOR': [
        {'name': 'Dashboard', 'icon': '📊', 'key': 'dashboard'},
    ],
}


def get_menu_items() -> list:
    """
    Obtiene los items del menú según el rol del usuario.
    
    Returns:
        Lista de items del menú
    """
    role = get_user_role()
    return MENU_ITEMS.get(role, [])


def render_sidebar() -> str:
    """
    Renderiza el sidebar de navegación.
    
    Returns:
        Clave de la página seleccionada
    """
    user = get_current_user()
    
    if not user:
        return 'login'
    
    with st.sidebar:
        # Logo y título
        st.markdown("## CamBus")
        st.caption("Centro de Distribución Mabe SLP")
        st.markdown("---")
        
        # Información del usuario
        st.markdown("### Usuario")
        st.markdown(f"**{user.get('nombre', 'Usuario')}**")
        
        # Badge del rol con colores
        role = user.get('rol', 'OPERADOR')
        role_colors = {
            'ADMIN': '🔴',
            'SUPERVISOR': '🟡',
            'OPERADOR': '🟢'
        }
        role_icon = role_colors.get(role, '⚪')
        st.markdown(f"{role_icon} {role}")
        
        st.markdown("---")
        
        # Menú de navegación
        st.markdown("### Menú")
        
        menu_items = get_menu_items()
        
        # Inicializar página seleccionada si no existe
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'dashboard'
        
        # Crear botones de navegación
        for item in menu_items:
            # Determinar si es la página actual
            is_active = st.session_state.current_page == item['key']
            
            # Estilo para página activa
            if is_active:
                btn_type = "primary"
            else:
                btn_type = "secondary"
            
            if st.button(
                f"{item['icon']} {item['name']}",
                key=f"nav_{item['key']}",
                use_container_width=True,
                type=btn_type
            ):
                st.session_state.current_page = item['key']
                st.rerun()
        
        st.markdown("---")
        
        # Información adicional solo para ADMIN
        if has_permission(['ADMIN']):
            with st.expander("Sistema"):
                st.caption("**Versión:** 1.0.0")
                st.caption("**Base de datos:** PostgreSQL")
                st.caption("**Framework:** Streamlit")
        
        # Toggle de modo oscuro
        st.markdown("---")
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
        
        dark_mode = st.toggle(
            "Modo Oscuro",
            value=st.session_state.dark_mode,
            help="Cambiar entre tema claro y oscuro"
        )
        
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        # Botón de cerrar sesión
        st.markdown("---")
        if st.button("Cerrar Sesión", use_container_width=True, type="secondary"):
            logout()
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.caption("© 2026 CamBus - Mabe")
    
    return st.session_state.current_page


def can_access_page(page_key: str) -> bool:
    """
    Verifica si el usuario puede acceder a una página.
    
    Args:
        page_key: Clave de la página
    
    Returns:
        True si tiene acceso
    """
    menu_items = get_menu_items()
    allowed_pages = [item['key'] for item in menu_items]
    return page_key in allowed_pages
