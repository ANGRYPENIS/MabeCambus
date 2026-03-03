# 🚛 CamBus - Control de Acceso Vehicular

Sistema de gestión de entrada y salida de vehículos para el Centro de Distribución Mabe SLP.

## 📋 Descripción

CamBus es una aplicación web desarrollada con Streamlit que permite:

- **Dashboard en tiempo real**: Visualización del estado de 100 andenes con auto-refresh cada 5 segundos
- **Registro manual de vehículos**: Entrada y salida de vehículos manualmente
- **Reportes y análisis**: Flujo por hora, eficiencia de andenes, tiempos de permanencia
- **Administración**: Gestión de usuarios, andenes, cámaras y backups

## 🛠️ Requisitos

- **Python 3.9+** - Descargar desde [python.org](https://python.org)
- **PostgreSQL 12+** - Descargar desde [postgresql.org](https://www.postgresql.org/download/windows/)
  - Durante la instalación, recuerda la contraseña del usuario `postgres`
  - Asegúrate que PostgreSQL corra en puerto `5432`
- **Git** (opcional) - Para clonar el repositorio
- **Docker** (opcional) - Para despliegue con contenedores (requiere Docker Desktop)

## 📦 Instalación

### ⚡ Instalación Rápida (Recomendado)

#### Windows:
```bash
# Doble-clic en setup.bat
# O abre CMD/PowerShell en la carpeta del proyecto y ejecuta:
setup.bat
```

#### Linux/Mac:
```bash
# Ejecutar el script
./setup.sh
```

Los scripts verificarán todo (Python, PostgreSQL) e instalarán automáticamente.  
Luego solo necesitas editar `.env` con tus credenciales de BD.

### Opción 1: Instalación Manual en Local

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
# Linux/Mac:
cp .env.example .env

# Windows (PowerShell):
Copy-Item .env.example .env

# Windows (CMD):
copy .env.example .env
```

Edita el archivo `.env` con tus credenciales de base de datos:
```
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

5. **Ejecutar la aplicación**

```bash
streamlit run app.py
```

La aplicación abrirá automáticamente en `http://localhost:8501`

La aplicación estará disponible en `http://localhost:8501`

### Opción 2: Despliegue con Docker

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
├── .git/                  # (Automático) Repositorio Git
├── .gitignore             # Archivos a ignorar en Git
├── setup.bat              # Instalación rápida (Windows)
├── setup.sh               # Instalación rápida (Linux/Mac)
├── run.bat                # Ejecutar la app (Windows)
├── run.sh                 # Ejecutar la app (Linux/Mac)
├── update.bat             # Actualizar (Windows)
├── update.sh              # Actualizar (Linux/Mac)
├── clean.bat              # Limpiar caché (Windows)
├── clean.sh               # Limpiar caché (Linux/Mac)
├── push.bat               # Commit + Push a GitHub (Windows)
├── push.sh                # Commit + Push a GitHub (Linux/Mac)
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

# Ejecutar tests (si existen)
pytest tests/

# Generar backup de base de datos
# Windows (PowerShell o CMD con pg_dump en PATH):
pg_dump -h localhost -U postgres cambus_db > backup.sql

# Linux/Mac:
pg_dump -h localhost -U postgres cambus_db > backup.sql

# Restaurar backup
# Windows:
psql -h localhost -U postgres cambus_db < backup.sql

# Linux/Mac:
psql -h localhost -U postgres cambus_db < backup.sql
```

### ⚠️ Nota para Windows: 
Si los comandos `pg_dump` y `psql` no funcionan, agrega la ruta de PostgreSQL a las variables de entorno del sistema, o usa la ruta completa:
```
"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe" -h localhost -U postgres cambus_db > backup.sql
```

## 📄 Licencia

© 2024 CamBus - Centro de Distribución Mabe SLP

---

**Desarrollado con ❤️ usando Streamlit**

## 📚 Documentación Complementaria

| Documento | Descripción |
|-----------|------------|
| **[GITHUB_SETUP.md](GITHUB_SETUP.md)** | Crear repositorio en GitHub y sincronizar proyecto |
| **[SCRIPTS_UTILIDAD.md](SCRIPTS_UTILIDAD.md)** | Guía de los scripts (`setup.bat`, `run.bat`, `update.bat`, `clean.bat`) |
| **[POSTGRESQL_WINDOWS.md](POSTGRESQL_WINDOWS.md)** | Instalación de PostgreSQL en Windows paso a paso |
| **[TROUBLESHOOTING_WINDOWS.md](TROUBLESHOOTING_WINDOWS.md)** | Solución de problemas comunes en Windows |
