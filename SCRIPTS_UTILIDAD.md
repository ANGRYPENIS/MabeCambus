# 🚀 Scripts de Utilidad - CamBus

Para simplificar la instalación, ejecución y mantenimiento de CamBus, se proporcionan scripts automatizados para **Windows**, **Linux** y **macOS**.

## 📋 Scripts Disponibles

### 1. **Setup** - Instalación Inicial

#### Windows
```cmd
setup.bat
```

#### Linux/Mac
```bash
./setup.sh
```

**¿Qué hace?**
- ✅ Verifica Python está instalado
- ✅ Verifica PostgreSQL (si falta, avisa)
- ✅ Crea entorno virtual automáticamente
- ✅ Instala todas las dependencias
- ✅ Crea archivo `.env` si no existe
- ✅ Guía paso a paso al final

**Cuándo ejecutar:** Una sola vez, al instalar por primera vez

---

### 2. **Run** - Ejecutar la Aplicación

#### Windows
```cmd
run.bat
```

#### Linux/Mac
```bash
./run.sh
```

**¿Qué hace?**
- ✅ Activa el entorno virtual automáticamente
- ✅ Verifica que PostgreSQL está disponible
- ✅ Inicia Streamlit
- ✅ Abre automáticamente en `http://localhost:8501`

**Cuándo ejecutar:** Cada vez que quieras usar la aplicación

---

### 3. **Update** - Actualizar Código y Dependencias

#### Windows
```cmd
update.bat
```

#### Linux/Mac
```bash
./update.sh
```

**¿Qué hace?**
- ✅ Activa el entorno virtual
- ✅ Tira `git pull` para obtener últimas actualizaciones (si Git está instalado)
- ✅ Actualiza dependencias Python a las últimas versiones
- ✅ Mantiene tu instalación siempre fresca

**Cuándo ejecutar:** Cuando haya nuevas actualizaciones disponibles

---

### 4. **Clean** - Limpiar Archivos Temporales

#### Windows
```cmd
clean.bat
```

#### Linux/Mac
```bash
./clean.sh
```

**¿Qué hace?**
- ✅ Elimina caché de Python (`__pycache__`)
- ✅ Elimina caché de Streamlit
- ✅ Elimina archivos `.pyc`
- ✅ Limpia carpetas `.egg-info`
- ✅ Libera espacio en disco

**Cuándo ejecutar:** 
- Cuando la app se comporta raro
- Cuando necesitas espacio en disco
- Antes de actualizar a una nueva versión

**⚠️ Nota:** Después de limpiar, la próxima ejecución será más lenta (recompila el código)

---

## 🎯 Flujo de Uso Recomendado

### Primera Vez (Instalación)

```
1. setup.bat  (o setup.sh en Linux/Mac)
2. Edita .env con tus credenciales
3. run.bat    (o run.sh)
```

### Uso Normal

```
1. run.bat    (o run.sh) cada vez que quieras usar la app
```

### Cuando Hay Actualizaciones

```
1. update.bat (o update.sh)
2. run.bat    (o run.sh)
```

### Problemas o Comportamiento Extraño

```
1. clean.bat  (o clean.sh)
2. run.bat    (o run.sh)
```

---

## 📊 Comparación: Script vs Manual

| Acción | Script | Manual |
|--------|--------|--------|
| Instalar | ✅ `setup.bat` | `python -m venv venv`, `pip install -r requirements.txt` |
| Ejecutar | ✅ `run.bat` | `venv\Scripts\activate`, `streamlit run app.py` |
| Actualizar | ✅ `update.bat` | `git pull`, `pip install --upgrade -r requirements.txt` |
| Limpiar | ✅ `clean.bat` | `rmdir /s venv`, manual cleanup |

**Los scripts ahorran tiempo y evitan errores**

---

## 🔧 Personalización

Si quieres cambiar el puerto o agregar más opciones, puedes editar los scripts:

### Windows (.bat)

En `run.bat`, cambia:
```bat
streamlit run app.py
```

A:
```bat
streamlit run app.py --server.port 8502
```

### Linux/Mac (.sh)

En `run.sh`, cambia:
```bash
streamlit run app.py
```

A:
```bash
streamlit run app.py --server.port 8502
```

---

## ⚠️ Problema: "Permission Denied" (Linux/Mac)

Si al ejecutar `./setup.sh` ves un error de permisos:

```bash
chmod +x setup.sh update.sh run.sh clean.sh
./setup.sh
```

---

## ⚠️ Problema: "Command Not Found" (Windows)

Si ves "No se reconoce como comando":

**Asegúrate de:**
1. Estar en la carpeta del proyecto: `cd C:\ruta\a\cambus`
2. Usar la extensión `.bat`: `setup.bat` (no `setup`)
3. Si aún falla, usa la ruta completa: `.\setup.bat`

---

## 📚 Documentación Relacionada

- [README.md](README.md) - Instrucciones generales
- [POSTGRESQL_WINDOWS.md](POSTGRESQL_WINDOWS.md) - Instalación de PostgreSQL en Windows
- [TROUBLESHOOTING_WINDOWS.md](TROUBLESHOOTING_WINDOWS.md) - Solución de problemas

---

**Última actualización:** Marzo 2026  
**Versión:** CamBus 1.0.0
