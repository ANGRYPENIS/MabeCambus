# 🐘 Configuración de PostgreSQL en Windows

## Instalación de PostgreSQL

### Descarga e Instalación

1. **Descarga PostgreSQL**
   - Ve a [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)
   - Descarga la versión más reciente (versión 16+ recomendada)

2. **Ejecuta el instalador**
   - Doble-clic en `postgresql-16-x64-installer.exe`

3. **Sigue el asistente:**

   | Paso | Valor Recomendado |
   |------|-----------------|
   | **Installation Directory** | Dejar default: `C:\Program Files\PostgreSQL\16` |
   | **Password** | Escribe un password seguro para el usuario `postgres` |
   | **Port** | Dejar default: `5432` |
   | **Locale** | Puede ser español o default |
   | **Data Directory** | Dejar default |

4. **Finaliza la instalación**
   - Deja desmarcado "Stack Builder"
   - Clic en Finish

---

## Verificar la Instalación

### Usando pgAdmin (Interfaz Gráfica)

1. **Abre pgAdmin**
   - Ve a Inicio > PostgreSQL > pgAdmin 4
   - O accede a `http://localhost:5050` en tu navegador

2. **Conéctate al servidor**
   - Password: la que configuraste en la instalación
   - Host: localhost
   - Puerto: 5432

3. **Verifica la conexión:**
   - En el panel izquierdo, expand "Servers"
   - Deberías ver "PostgreSQL 16" conectado

### Usando Línea de Comandos

```cmd
REM Abre PowerShell o CMD como Administrador

REM Conectarse al servidor
psql -h localhost -U postgres

REM Te pedirá el password, escríbelo
REM Si funciona, verás: postgres=#

REM Salir
\q
```

---

## Crear la Base de Datos

### Opción 1: Usando pgAdmin (Recomendado para principiantes)

1. **Abre pgAdmin**
2. **En el panel izquierdo:**
   - Clic derecho en "Databases"
   - Selecciona "Create > Database"
   
3. **En la ventana de creación:**
   - **Name:** `cambus_db`
   - Dejar otros campos con valores default
   - Clic en "Save"

4. **Crear tablas:**
   - Selecciona la BD `cambus_db`
   - Ve a Tools > Query Tool
   - Copia y pega el contenido de `cambus.sql`
   - Ejecuta (Ctrl+Enter o el botón de play)

### Opción 2: Usando Línea de Comandos

```cmd
REM Desde la carpeta del proyecto cambus

REM 1. Crear la base de datos
psql -h localhost -U postgres -c "CREATE DATABASE cambus_db"

REM 2. Crear las tablas
psql -h localhost -U postgres -d cambus_db -f cambus.sql

REM 3. Verificar que se creó
psql -h localhost -U postgres -d cambus_db -c "\dt"
```

---

## Configurar CamBus para conectarse a PostgreSQL

### 1. Editar el archivo `.env`

Abre `.env` en un editor de texto (Notepad, VSCode, etc.) y asegúrate que tenga:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cambus_db
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
```

Reemplaza `tu_password_aqui` con la contraseña que configuraste en PostgreSQL.

### 2. Editar `config.yaml` (si es necesario)

```yaml
database:
  host: "localhost"
  port: 5432
  name: "cambus_db"
  user: "postgres"
  password: ""  # Se carga desde .env
```

---

## Verificar la Conexión desde CamBus

```cmd
REM Activar entorno virtual
venv\Scripts\activate.bat

REM Ejecutar CamBus
streamlit run app.py
```

Si todo está bien, deberías ver:
- ✅ "Connected to PostgreSQL successfully" en la terminal
- ✅ La aplicación se abre en `http://localhost:8501`

---

## Problema: "could not translate host name "localhost" to address"

**Solución:** PostgreSQL no está corriendo

```cmd
REM Verificar si PostgreSQL está corriendo
psql -h localhost -U postgres -c "SELECT 1"

REM Si falla, abrir Services:
# Presiona Win+R, escribe "services.msc"
# Busca "postgresql-x64-16" (o tu versión)
# Si está detenido, clic derecho > Start
```

---

## Backup y Restauración

### Crear un Backup

```cmd
REM Desde cualquier carpeta
pg_dump -h localhost -U postgres cambus_db > backup.sql

REM Si no funciona pg_dump, usa la ruta completa:
"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe" -h localhost -U postgres cambus_db > backup.sql
```

### Restaurar un Backup

```cmd
REM Restaurar la BD desde backup
psql -h localhost -U postgres cambus_db < backup.sql

REM O usar la ruta completa:
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -h localhost -U postgres cambus_db < backup.sql
```

---

## Desinstalar y Limpiar

Si tienes problemas y quieres empezar de cero:

1. **Desinstala PostgreSQL:**
   - Inicio > Desinstalar un programa
   - Busca "PostgreSQL"
   - Selecciona y haz clic Desinstalar
   - Cuando pregunte, elige "Remove all" para limpiar datos

2. **Elimina datos residuales (opcional):**
   ```cmd
   REM PowerShell como Administrador
   Remove-Item "C:\Program Files\PostgreSQL" -Recurse -Force
   Remove-Item "$env:APPDATA\postgresql" -Recurse -Force
   ```

3. **Reinstala PostgreSQL** siguiendo los pasos anteriores

---

## Referencia Rápida

| Tarea | Comando |
|-------|---------|
| Conectar al servidor | `psql -h localhost -U postgres` |
| Conectar a BD específica | `psql -h localhost -U postgres -d cambus_db` |
| Crear BD | `psql -h localhost -U postgres -c "CREATE DATABASE cambus_db"` |
| Cargar script SQL | `psql -h localhost -U postgres -d cambus_db -f archivo.sql` |
| Listar tablas | `psql -h localhost -U postgres -d cambus_db -c "\dt"` |
| Hacer backup | `pg_dump -h localhost -U postgres cambus_db > backup.sql` |
| Restaurar backup | `psql -h localhost -U postgres cambus_db < backup.sql` |

---

**Última actualización:** Marzo 2026  
**Versión:** CamBus 1.0.0
