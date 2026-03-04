# Cambios Realizados - Database Configuration Scripts

## 📋 Resumen

Se han actualizado y mejorado significativamente los scripts `configure-db.bat` y `configure-db.sh` para proporcionar funcionalidad completa de base de datos, incluyendo la capacidad de crear nuevas bases de datos, usuarios PostgreSQL, y cuentas de demostración automáticamente.

---

## ✨ Nuevas Características

### 1. **Menú de Opciones**
El script ahora presenta un menú interactivo con dos opciones principales:

```
MENU DE OPCIONES:
  1. Usar base de datos existente
  2. Crear nueva base de datos
  0. Salir
```

### 2. **Opción 1: Usar Base de Datos Existente**
- Conectarse a una base de datos PostgreSQL ya existente
- Validar la conexión
- Crear/actualizar cuenta de demostración automáticamente
- Generar archivo `.env`

### 3. **Opción 2: Crear Nueva Base de Datos** ⭐ NEW
Flujo completo de inicialización:
- Pedir credenciales de administrador PostgreSQL
- Crear nuevo usuario PostgreSQL con contraseña
- Crear nueva base de datos
- **Cargar automáticamente el esquema SQL desde `cambus.sql`** ⭐
- Crear cuenta de demostración
- Generar archivo `.env`

### 4. **Creación Automática de Usuario Demo** ⭐ NEW
Cada configuración crea automáticamente una cuenta de demostración:

| Campo | Valor |
|-------|-------|
| **Username** | `demo` |
| **Password** | `demo_password` |
| **Role** | `OPERADOR` |
| **Departament** | `DEMOSTRACION` |
| **Status** | Activo |

---

## 📂 Archivos Nuevos/Modificados

### Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `configure-db.bat` | ✅ Rediseñado completamente con menú + opciones |
| `configure-db.sh` | ✅ Rediseñado completamente con menú + opciones |

**Antes:** Solo permitía seleccionar BD existente  
**Ahora:** Puede crear BD nueva con user + cargar schema + crear demo user

### Archivos Nuevos

| Archivo | Descripción |
|---------|-------------|
| `DATABASE_SETUP.md` | 📖 Guía completa de configuración de base de datos |
| `create-demo-users.sql` | 🗄️ Script SQL opcional para crear usuarios demo adicionales |

### Archivos Actualizados

| Archivo | Cambios |
|---------|---------|
| `README.md` | ✅ Agregada "Opción 1" de instalación rápida con scripts |

---

## 🚀 Uso Rápido

### Windows

```bash
# Paso 1: Configurar BD (crea .env)
configure-db.bat

# Cuando pregunte, selecciona opción 2 para crear BD nueva
# O opción 1 si ya tienes una BD existente

# Paso 2: Instalar dependencias
setup.bat

# Paso 3: Ejecutar aplicación
run.bat

# Paso 4: Acceder en navegador
# http://localhost:8501
# Username: demo
# Password: demo_password
```

### Linux / macOS

```bash
# Paso 1: Configurar BD
./configure-db.sh

# Paso 2: Instalar dependencias
./setup.sh

# Paso 3: Ejecutar aplicación
./run.sh

# Paso 4: Acceder en navegador
# http://localhost:8501
# Username: demo
# Password: demo_password
```

---

## 🔧 Flujo de Creación de BD Nueva

```
┌─────────────────────────────────────────┐
│  configure-db.bat / configure-db.sh     │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
    Opción 1         Opción 2
       │           (Crear Nueva)
       │                │
       │        ┌───────┴────────┐
       │        ▼                ▼
       │   Pedir Creds        Solicitar:
       │   Admin PG         - Nombre BD
       │        │           - User PostgreSQL
       │        │           - Password
       │        │                │
       │        │        ┌───────┴────────┐
       │        │        ▼                ▼
       │        │    Crear User    Crear Database
       │        │        │                │
       │        │        └────────┬───────┘
       │        │                 ▼
       │        │          Cargar cambus.sql
       │        │          (Crear tablas,
       │        │           vistas, funciones)
       │        │                 │
       │        └────────┬────────┘
       │                 ▼
       │         Crear usuario demo
       │                 │
       └────────┬────────┘
               ▼
         Validar conexión
               │
               ▼
         Generar .env
               │
               ▼
          ✅ Completado
```

---

## 🔑 Cambios Técnicos

### Script Windows (configure-db.bat)

**Cambios principales:**
- Agregadas funciones de menú `:use_existing` y `:create_new`
- Implementada lógica de creación de usuario PostgreSQL con `CREATE USER`
- Implementada lógica de creación de base de datos con `CREATE DATABASE`
- Agregada ejecución de `psql -f cambus.sql` para cargar esquema
- Mejorado manejo de variables con `setlocal enabledelayedexpansion`
- Agregadas validaciones de conexión antes de guardar `.env`

**Líneas de código:** ~350 (antes: ~100)

### Script Linux/Mac (configure-db.sh)

**Cambios principales:**
- Convertidas a funciones modulares y reutilizables
- Agregado parámetro `case` para selección de menú
- Implementada creación de usuario y BD con heredoc de psql
- Ejecución de `psql -f cambus.sql` para cargar esquema
- Mejorado parsing de output psql con `awk` y `sed`
- Agregadas validaciones de conexión

**Líneas de código:** ~280 (antes: ~150)

---

## 🎯 Casos de Uso

### Caso 1: Usuario sin BD existente (Más común)
```
Usuario ejecuta: configure-db.bat
Selecciona: Opción 2 (Crear nueva BD)
Proporciona:
  - Admin credentials (ej: postgres / postgres_pass)
  - Nombre BD: cambus_db
  - Usuario nuevo: cambus_user
  - Contraseña: mi_contraseña_segura

Resultado:
  ✅ BD creada
  ✅ Usuario creado
  ✅ Esquema cargado (tablas, índices, funciones)
  ✅ Demo user creado
  ✅ .env generado
  ✅ Listo para: setup.bat > run.bat
```

### Caso 2: Usuario con BD ya existente
```
Usuario ejecuta: configure-db.bat
Selecciona: Opción 1 (Usar existente)
Proporciona:
  - Host: localhost
  - Port: 5432
  - Username: postgres
  - Password: postgres_pass
  - Database: cambus_db

Resultado:
  ✅ Valida conexión
  ✅ Demo user creado
  ✅ .env generado
  ✅ Listo para: setup.bat > run.bat
```

---

## 🆕 SQL Script para Demo Users (create-demo-users.sql)

Nuevo archivo SQL permite crear usuarios demo adicionales con diferentes roles:

```sql
-- Crear 3 cuentas demo (todas con contraseña: demo_password)

-- usuario: demo (OPERADOR) - Read-only
-- usuario: supervisor_demo (SUPERVISOR) - Dashboard + Reports
-- usuario: admin_demo (ADMIN) - Full access
```

**Cómo usar:**
```bash
# Conectarse a la BD y ejecutar:
psql -h localhost -U cambus_user -d cambus_db -f create-demo-users.sql
```

---

## 📖 Documentación

Se agregó completa documentación en `DATABASE_SETUP.md`:

- ✅ Requisitos previos
- ✅ Instrucciones plataforma-específicas (Windows/Linux/macOS)
- ✅ Flujo de cada opción paso a paso
- ✅ Explicación de qué se crea en la BD
- ✅ Detalles del usuario demo
- ✅ Formato de archivo `.env`
- ✅ Troubleshooting completo
- ✅ Cómo reconfigura o resetear

---

## ✅ Validación

### ✓ Windows (Batch)
- Sintaxis válida de batch
- Compatible con Windows 7+
- Manejo correcto de variables con espacios
- Errorlevel checks implementados

### ✓ Linux/Mac (Bash)
- Compatible con bash 4+
- Uso de `${variable:-default}` para defaults
- Heredoc para multi-línea SQL
- Permisos ejecutables: `chmod +x *.sh`

### ✓ Funcionalidad
- ✅ Conexión a PostgreSQL validada
- ✅ Creación de usuario probada
- ✅ Creación de BD probada
- ✅ Carga de SQL probada
- ✅ Generación de .env probada

---

## 🔐 Seguridad

### Demo Account Security
- Contraseña hasheada con bcrypt (12 rounds)
- Hash: `$2b$12$YY7GWLRVHMPXkc9iOvN/NeHEbKKW6SH1lWHPEqPjKsHwSHVqXFU3G`
- ⚠️ Cambiar antes de producción
- Solo rol OPERADOR (menos permisos)

### Script Security
- No guarda contraseñas en scripts
- .env en .gitignore (no se commitea)
- Valida conexión antes de guardar config
- Crea backups automáticos de .env anterior

---

## 📦 Requisitos

- **Windows**: PostgreSQL installed con psql en PATH
- **Linux/Mac**: PostgreSQL installed con acceso a psql
- **Archivo**: `cambus.sql` debe existir en mismo directorio

---

## 🎓 Próximos Pasos

Después de ejecutar `configure-db`:

1. **Instalar dependencias:**
   - Windows: `setup.bat`
   - Linux/Mac: `./setup.sh`

2. **Ejecutar aplicación:**
   - Windows: `run.bat`
   - Linux/Mac: `./run.sh`

3. **Acceder a:**
   - URL: `http://localhost:8501`
   - Username: `demo`
   - Password: `demo_password`

4. **Cambiar relaciones de producción:**
   - Crear usuario ADMIN con contraseña segura
   - Cambiar contraseña de demo user o eliminar
   - Importar datos reales de BD

---

## 📞 Soporte

- **Guía completa:** [DATABASE_SETUP.md](DATABASE_SETUP.md)
- **Solución de problemas:** [TROUBLESHOOTING_WINDOWS.md](TROUBLESHOOTING_WINDOWS.md)
- **PostgreSQL docs:** https://www.postgresql.org/docs/
