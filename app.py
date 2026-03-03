"""
============================================================================
CamBus - Aplicación Principal
Centro de Distribución Mabe SLP
============================================================================
Sistema de Control de Acceso Vehicular

Autor: CamBus Team
Versión: 1.0.0
============================================================================
"""

import streamlit as st
import os
import sys

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.auth import (
    init_session_state,
    is_authenticated,
    render_login_page,
    has_permission
)
from components.sidebar import render_sidebar, can_access_page
from pages.dashboard import render_dashboard
from pages.registro import render_registro
from pages.reportes import render_reportes
from pages.admin import render_admin


# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="CamBus - Control de Acceso Vehicular",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': """
        ## 🚛 CamBus - Control de Acceso Vehicular
        
        Sistema de gestión de entrada y salida de vehículos
        para el Centro de Distribución Mabe SLP.
        
        **Versión:** 1.0.0
        
        © 2024 CamBus - Mabe
        """
    }
)


# ============================================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================================

def get_css_styles(dark_mode: bool = False) -> str:
    """Genera los estilos CSS según el modo de tema"""
    
    if dark_mode:
        # Modo Oscuro
        bg_color = "#0e1117"
        secondary_bg = "#262730"
        sidebar_bg = "#1a1d24"
        text_color = "#fafafa"
        text_secondary = "#b0b0b0"
        header_color = "#4da6ff"
        subheader_color = "#a0a0a0"
        card_bg = "#1a1d24"
        card_shadow = "rgba(255,255,255,0.05)"
        input_bg = "#262730"
        input_border = "#404040"
        input_text = "#fafafa"
        label_color = "#fafafa"
        success_bg = "#1e3a2f"
        success_border = "#2d5a45"
        success_text = "#4ade80"
        error_bg = "#3a1e1e"
        error_border = "#5a2d2d"
        error_text = "#f87171"
        table_header_bg = "#262730"
        table_row_bg = "#1a1d24"
        table_border = "#404040"
        link_color = "#4da6ff"
        button_secondary_bg = "#262730"
        button_secondary_text = "#fafafa"
        expander_bg = "#1a1d24"
        metric_label = "#b0b0b0"
        metric_value = "#fafafa"
    else:
        # Modo Claro
        bg_color = "#ffffff"
        secondary_bg = "#f0f2f6"
        sidebar_bg = "#f0f2f6"
        text_color = "#262730"
        text_secondary = "#666666"
        header_color = "#1f77b4"
        subheader_color = "#666666"
        card_bg = "#f8f9fa"
        card_shadow = "rgba(0,0,0,0.1)"
        input_bg = "#ffffff"
        input_border = "#e0e0e0"
        input_text = "#262730"
        label_color = "#262730"
        success_bg = "#d4edda"
        success_border = "#c3e6cb"
        success_text = "#155724"
        error_bg = "#f8d7da"
        error_border = "#f5c6cb"
        error_text = "#721c24"
        table_header_bg = "#f0f2f6"
        table_row_bg = "#ffffff"
        table_border = "#e0e0e0"
        link_color = "#1f77b4"
        button_secondary_bg = "#f0f2f6"
        button_secondary_text = "#262730"
        expander_bg = "#f8f9fa"
        metric_label = "#666666"
        metric_value = "#262730"
    
    return f"""
    <style>
        /* Ocultar menú de hamburguesa, footer y navegación automática de páginas */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stSidebarNav"] {{display: none !important;}}
        
        /* === FONDO PRINCIPAL === */
        .stApp {{
            background-color: {bg_color} !important;
        }}
        
        /* === SIDEBAR === */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
        }}
        
        [data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: {text_color} !important;
        }}
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {{
            color: {text_color} !important;
        }}
        
        /* === TEXTOS GENERALES === */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
            color: {text_color} !important;
        }}
        
        .stApp p, .stApp span, .stApp div {{
            color: {text_color};
        }}
        
        .stMarkdown, .stText {{
            color: {text_color} !important;
        }}
        
        /* === LABELS DE INPUTS === */
        .stTextInput label, 
        .stSelectbox label, 
        .stMultiselect label,
        .stTextArea label,
        .stNumberInput label,
        .stDateInput label,
        .stTimeInput label,
        .stCheckbox label,
        .stRadio label,
        [data-testid="stWidgetLabel"] {{
            color: {label_color} !important;
        }}
        
        /* === INPUTS Y SELECTBOX === */
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {input_border} !important;
        }}
        
        .stSelectbox > div > div,
        .stMultiselect > div > div {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {input_border} !important;
        }}
        
        [data-testid="stSelectbox"] {{
            color: {text_color} !important;
        }}
        
        /* === MÉTRICAS === */
        [data-testid="stMetricLabel"] {{
            color: {metric_label} !important;
        }}
        
        [data-testid="stMetricValue"] {{
            color: {metric_value} !important;
        }}
        
        [data-testid="stMetricDelta"] {{
            color: {text_secondary} !important;
        }}
        
        /* === TABS === */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {secondary_bg} !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {text_color} !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            color: {header_color} !important;
        }}
        
        /* === EXPANDERS === */
        .streamlit-expanderHeader {{
            background-color: {expander_bg} !important;
            color: {text_color} !important;
        }}
        
        [data-testid="stExpander"] {{
            background-color: {expander_bg} !important;
            border-color: {input_border} !important;
        }}
        
        [data-testid="stExpander"] * {{
            color: {text_color} !important;
        }}
        
        /* === TABLAS Y DATAFRAMES === */
        .stDataFrame {{
            background-color: {table_row_bg} !important;
        }}
        
        [data-testid="stDataFrame"] {{
            color: {text_color} !important;
        }}
        
        .stDataFrame thead tr th {{
            background-color: {table_header_bg} !important;
            color: {text_color} !important;
            border-color: {table_border} !important;
        }}
        
        .stDataFrame tbody tr td {{
            background-color: {table_row_bg} !important;
            color: {text_color} !important;
            border-color: {table_border} !important;
        }}
        
        /* === BOTONES === */
        .stButton button[kind="secondary"] {{
            background-color: {button_secondary_bg} !important;
            color: {button_secondary_text} !important;
        }}
        
        /* === HEADER PERSONALIZADO === */
        .main-header {{
            font-size: 2.5rem;
            font-weight: bold;
            color: {header_color} !important;
            text-align: center;
            padding: 1rem 0;
            margin-bottom: 1rem;
        }}
        
        .sub-header {{
            font-size: 1.2rem;
            color: {subheader_color} !important;
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        /* === TARJETAS === */
        .metric-card {{
            background-color: {card_bg} !important;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 2px 4px {card_shadow};
        }}
        
        /* === MAPA DE ANDENES === */
        .anden-box {{
            border-radius: 5px;
            padding: 5px;
            text-align: center;
            min-height: 60px;
            margin: 2px;
            font-size: 11px;
        }}
        
        /* === ESTADOS DE ANDENES === */
        .estado-libre {{
            background-color: #28a745;
            color: white !important;
        }}
        
        .estado-ocupado {{
            background-color: #dc3545;
            color: white !important;
        }}
        
        .estado-mantenimiento {{
            background-color: #ffc107;
            color: black !important;
        }}
        
        .estado-bloqueado {{
            background-color: #343a40;
            color: white !important;
        }}
        
        /* === MENSAJES === */
        .success-message {{
            background-color: {success_bg} !important;
            border-color: {success_border} !important;
            color: {success_text} !important;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}
        
        .error-message {{
            background-color: {error_bg} !important;
            border-color: {error_border} !important;
            color: {error_text} !important;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}
        
        /* === LINKS === */
        a {{
            color: {link_color} !important;
        }}
        
        /* === TOOLTIPS === */
        [data-testid="stTooltipIcon"] {{
            color: {text_secondary} !important;
        }}
        
        /* === CAPTIONS === */
        .stCaption, [data-testid="caption"] {{
            color: {text_secondary} !important;
        }}
        
        /* === FORM === */
        [data-testid="stForm"] {{
            background-color: {secondary_bg} !important;
            border-color: {input_border} !important;
        }}
        
        /* === INFO/WARNING/ERROR BOXES === */
        .stAlert {{
            color: {text_color} !important;
        }}
        
        /* === DIVIDER === */
        hr {{
            border-color: {input_border} !important;
        }}
        
        /* === CHECKBOX/TOGGLE === */
        .stCheckbox span, .stToggle span {{
            color: {text_color} !important;
        }}
    </style>
    """


def apply_theme():
    """Aplica el tema según la preferencia del usuario"""
    dark_mode = st.session_state.get('dark_mode', False)
    st.markdown(get_css_styles(dark_mode), unsafe_allow_html=True)


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def render_header():
    """Renderiza el header de la aplicación"""
    st.markdown("""
    <div class="main-header">
        🚛 CamBus - Control de Acceso Vehicular
    </div>
    <div class="sub-header">
        Centro de Distribución Mabe SLP
    </div>
    """, unsafe_allow_html=True)


def render_page(page_key: str):
    """
    Renderiza la página según la clave seleccionada.
    
    Args:
        page_key: Clave de la página a renderizar
    """
    # Verificar permisos
    if not can_access_page(page_key):
        st.error("🚫 No tiene permisos para acceder a esta página")
        return
    
    # Renderizar página correspondiente
    if page_key == 'dashboard':
        render_dashboard()
    elif page_key == 'registro':
        # Solo ADMIN y SUPERVISOR pueden acceder
        if has_permission(['ADMIN', 'SUPERVISOR']):
            render_registro()
        else:
            st.error("🚫 No tiene permisos para acceder a esta página")
    elif page_key == 'reportes':
        # Solo ADMIN y SUPERVISOR pueden acceder
        if has_permission(['ADMIN', 'SUPERVISOR']):
            render_reportes()
        else:
            st.error("🚫 No tiene permisos para acceder a esta página")
    elif page_key == 'admin':
        # Solo ADMIN puede acceder
        if has_permission(['ADMIN']):
            render_admin()
        else:
            st.error("🚫 No tiene permisos para acceder a esta página")
    else:
        st.warning("⚠️ Página no encontrada")
        render_dashboard()


# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal de la aplicación"""
    # Inicializar estado de sesión
    init_session_state()
    
    # Aplicar tema (claro/oscuro)
    apply_theme()
    
    # Verificar autenticación
    if not is_authenticated():
        # Mostrar página de login
        render_header()
        render_login_page()
    else:
        # Usuario autenticado - mostrar aplicación
        # Renderizar sidebar y obtener página seleccionada
        current_page = render_sidebar()
        
        # Renderizar header
        render_header()
        
        # Renderizar página seleccionada
        render_page(current_page)


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()
