# 🪟 Guía de Troubleshooting - Windows

## Problemas Comunes y Soluciones

### 1. "Python no reconocido como comando"

**Problema:** Al ejecutar `python` o `python -m venv`, aparece error

**Soluciones:**

a) **Reinstalar Python con opción PATH activa:**
   - Descarga Python desde [python.org](https://python.org)
   - En el instalador, marca la opción **"Add Python to PATH"**
   - Reinicia la terminal después de instalar

b) **Verificar la instalación:**
   ```cmd
   python --version
   ```

c) **Usar la ruta completa:**
   ```cmd
   "C:\Program Files\Python311\python.exe" --version
   ```

---

### 2. "PostgreSQL no reconocido"

**Problema:** `psql` o `pg_dump` no funcionan

**Soluciones:**

a) **Agregar PostgreSQL al PATH de Windows:**
   - Abre Variables de Entorno (System Properties > Environment Variables)
   - Haz clic en "Edit PATH"
   - Agrega: `C:\Program Files\PostgreSQL\16\bin` (ajusta versión si es diferente)
   - Reinicia CMD/PowerShell

b) **Usar la ruta completa:**
   ```cmd
   "C:\Program Files\PostgreSQL\16\bin\psql.exe" -h localhost -U postgres -d cambus_db
   ```

c) **Instalar PostgreSQL si no está:**
   - Descarga desde [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)
   - Recuerda el password del usuario `postgres`
   - Asegúrate que corre en puerto `5432`

---

### 3. "Could not connect to database"

**Problema:** La app no puede conectarse a PostgreSQL

**Soluciones:**

a) **Verificar que PostgreSQL está corriendo:**
   - Abre "Services" (services.msc)
   - Busca "postgresql-x64-16" o similar
   - Asegúrate que el estado es "Running"

b) **Verificar credenciales en .env:**
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=cambus_db
   DB_USER=postgres
   DB_PASSWORD=tu_contraseña_aqui
   ```

c) **Probar conexión manual:**
   ```cmd
   psql -h localhost -U postgres -c "SELECT 1"
   ```
   Deberá pedir password y mostrar el resultado

d) **Crear la base de datos si no existe:**
   ```cmd
   psql -h localhost -U postgres -f cambus.sql
   ```

---

### 4. "Module not found" (pip install falla)

**Problema:** Error al instalar dependencias

**Soluciones:**

a) **Actualizar pip, setuptools y wheel:**
   ```cmd
   python -m pip install --upgrade pip setuptools wheel
   ```

b) **Instalar requirements con verbose:**
   ```cmd
   pip install -r requirements.txt -v
   ```

c) **Instalar paquetes individuales:**
   ```cmd
   pip install streamlit pandas psycopg2-binary sqlalchemy plotly bcrypt python-dotenv pyyaml
   ```

---

### 5. "Streamlit port already in use"

**Problema:** Puerto 8501 ya está ocupado

**Soluciones:**

a) **Cambiar el puerto:**
   ```cmd
   streamlit run app.py --server.port 8502
   ```

b) **Matar el proceso que usa el puerto:**
   ```cmd
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   ```

---

### 6. "Permission denied" o problemas de permisos

**Problema:** No puedes crear archivos o ejecutar el script

**Soluciones:**

a) **Ejecutar CMD/PowerShell como Administrador**

b) **Para el script setup.bat:**
   - Haz clic derecho en setup.bat
   - Selecciona "Run as administrator"

c) **En PowerShell, permitir scripts:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

---

### 7. "Encoding error" al leer config.yaml

**Problema:** Error de codificación al cargar configuración

**Soluciones:**

a) **El código ya está arreglado para usar UTF-8**
   - Asegúrate de usar la última versión

b) **Verificar que config.yaml está en UTF-8:**
   - Abre con Notepad++
   - Menú: Encoding > UTF-8

---

### 8. Virtualenv no se activa correctamente

**Problema:** Después de `venv\Scripts\activate.bat` no ves cambios

**Soluciones:**

a) **Verificar que el script estuvocorrectamente:**
   ```cmd
   venv\Scripts\activate.bat
   echo %VIRTUAL_ENV%
   ```
   Debería mostrar la ruta del venv

b) **En PowerShell, ejecutar:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

c) **Si falla por política de ejecución:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\venv\Scripts\Activate.ps1
   ```

---

## Verificación Completa

Para asegurar que todo funciona, ejecuta:

```cmd
REM Activar venv
venv\Scripts\activate.bat

REM Verificar Python y paquetes
python --version
pip list | findstr streamlit
pip list | findstr psycopg2

REM Verificar PostgreSQL
psql --version
psql -h localhost -U postgres -c "SELECT 1"

REM Verificar archivos de configuración
type .env
type config.yaml
```

---

## ¿Todavía hay problemas?

1. Verifica que tienes **Python 3.9+**
2. Verifica que tienes **PostgreSQL 12+** corriendo
3. Verifica que el archivo **.env está correctamente configurado**
4. Revisa los logs en la terminal para mensajes de error específicos
5. Intenta ejecutar en una carpeta sin espacios en el nombre

---

**Última actualización:** Marzo 2026  
**Versión:** CamBus 1.0.0
