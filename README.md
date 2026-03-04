# 🚛 CamBus - Control de Acceso Vehicular

Sistema de gestión de entrada y salida de vehículos para el Centro de Distribución Mabe SLP.

## 📋 Descripción

CamBus es una aplicación web desarrollada con Streamlit que permite:

- **Dashboard en tiempo real**: Visualización del estado de 100 andenes con auto-refresh cada 5 segundos
- **Registro manual de vehículos**: Entrada y salida de vehículos manualmente
- **Reportes y análisis**: Flujo por hora, eficiencia de andenes, tiempos de permanencia
- **Administración**: Gestión de usuarios, andenes, cámaras y backups

## 🛠️ Requisitos

- Python 3.9+
- PostgreSQL 12+
- Docker (opcional, para despliegue con contenedores)

## 📦 Instalación

### ⭐ Opción 1: Instalación Rápida con Scripts (Recomendado)

La forma más fácil para usuarios de Windows/Linux/Mac. Los scripts automatizan todo el proceso.

#### Windows

```bash
# 1. Configurar base de datos (crea .env automáticamente)
configure-db.bat

# 2. Instalar dependencias Python
setup.bat

# 3. Ejecutar la aplicación
run.bat
```

#### Linux / macOS

```bash
# 1. Configurar base de datos (crea .env automáticamente)
./configure-db.sh

# 2. Instalar dependencias Python
./setup.sh

# 3. Ejecutar la aplicación
./run.sh
```

**La aplicación estará disponible en** `http://localhost:8501`

**Login con cuenta demo:**
- Usuario: `demo`
- Contraseña: `demo_password`

[Guía detallada de configuración](DATABASE_SETUP.md)

### Opción 2: Instalación Manual

1. **Clonar o copiar el proyecto**

```bash
cd /ruta/al/proyecto/cambus
```

2. **Crear entorno virtual**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

```bash
cp .env.example .env
# Editar .env con tus credenciales de base de datos
```

5. **Ejecutar la aplicación**

```bash
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`

### Opción 3: Despliegue con Docker

1. **Construir y ejecutar con Docker Compose**

```bash
docker-compose up --build -d
```

2. **Para incluir Adminer (administrador web de BD)**

```bash
docker-compose --profile tools up -d
```

La aplicación estará disponible en:
- CamBus: `http://localhost:8501`
- Adminer (opcional): `http://localhost:8080`

## 📊 Utilidades y Scripts

Además de los scripts de instalación, incluyen herramientas útiles:

| Script | Plataforma | Descripción |
|--------|-----------|-------------|
| `configure-db` | Win/Lin/Mac | 🗄️ Configurar base de datos (crear o usar existente) |
| `setup` | Win/Lin/Mac | 📦 Instalar dependencias Python |
| `run` | Win/Lin/Mac | ▶️ Ejecutar la aplicación |
| `update` | Win/Lin/Mac | 🔄 Actualizar dependencias |
| `clean` | Win/Lin/Mac | 🧹 Limpiar archivos temporales y cache |
| `push` | Win/Lin/Mac | 📤 Subir cambios a GitHub |
| `check-postgres` | Win/Lin/Mac | ✅ Verificar instalación de PostgreSQL |

**Ver:** [Scripts Útiles](SCRIPTS_UTILIDAD.md)

## 🗄️ Base de Datos

La aplicación espera las siguientes tablas en PostgreSQL:

- `usuarios` - Gestión de usuarios del sistema
- `andenes` - Catálogo de andenes
- `camaras` - Catálogo de cámaras
- `registros_vehiculos` - Registro de entrada/salida
- `estancias_vehiculos` - Historial de estancias

### Vistas requeridas:
- `vw_dashboard_tiempo_real`
- `vw_flujo_horario`
- `vw_eficiencia_andenes`
- `vw_productos_mas_movidos`

### Funciones requeridas:
- `registrar_entrada_vehiculo()`
- `registrar_salida_vehiculo()`

## 👥 Roles de Usuario

| Rol | Dashboard | Registro | Reportes | Admin |
|-----|-----------|----------|----------|-------|
| ADMIN | ✅ | ✅ | ✅ | ✅ |
| SUPERVISOR | ✅ | ✅ | ✅ | ❌ |
| OPERADOR | ✅ (solo lectura) | ❌ | ❌ | ❌ |

## 📁 Estructura del Proyecto

```
cambus/
├── app.py                 # Aplicación principal
├── config.yaml            # Configuración
├── requirements.txt       # Dependencias
├── Dockerfile            # Imagen Docker
├── docker-compose.yml    # Orquestación Docker
├── .env.example          # Variables de entorno ejemplo
├── .streamlit/
│   └── config.toml       # Configuración Streamlit
├── utils/
│   ├── __init__.py
│   ├── db.py             # Conexión a base de datos
│   └── auth.py           # Autenticación
├── components/
│   ├── __init__.py
│   └── sidebar.py        # Barra lateral de navegación
└── pages/
    ├── __init__.py
    ├── dashboard.py      # Dashboard principal
    ├── registro.py       # Registro de vehículos
    ├── reportes.py       # Reportes y análisis
    └── admin.py          # Administración
```

## ⚙️ Configuración

### config.yaml

```yaml
database:
  host: "localhost"
  port: 5432
  name: "cambus_db"
  user: "postgres"
  password: ""  # Usar variable de entorno DB_PASSWORD
```

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| DB_PASSWORD | Contraseña de PostgreSQL | - |
| DB_HOST | Host de PostgreSQL | localhost |
| DB_PORT | Puerto de PostgreSQL | 5432 |
| DB_NAME | Nombre de la base de datos | cambus_db |
| DB_USER | Usuario de PostgreSQL | postgres |

## 🔐 Seguridad

- Las contraseñas se almacenan con hash bcrypt (12 rounds)
- Sesiones manejadas con `st.session_state`
- Máximo 5 intentos de login fallidos
- Validación de permisos por rol

## 🚀 Comandos Útiles

```bash
# Ejecutar en modo desarrollo con auto-reload
streamlit run app.py --server.runOnSave true

# Ejecutar tests
pytest tests/

# Generar backup de base de datos
pg_dump -h localhost -U postgres cambus_db > backup.sql

# Restaurar backup
psql -h localhost -U postgres cambus_db < backup.sql
```

## 📄 Licencia

© 2024 CamBus - Centro de Distribución Mabe SLP

---

**Desarrollado con ❤️ usando Streamlit**
