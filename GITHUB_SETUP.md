# 🐙 GitHub Setup - CamBus

Guía completa para crear un repositorio en GitHub y mantener tu proyecto sincronizado.

---

## 📋 Requisitos Previos

1. **Cuenta en GitHub**
   - Crear en [github.com](https://github.com) si no tienes
   - Básico: Gratis
   - Privado: Gratis (sin límite de repos privados desde 2019)

2. **Git instalado localmente**
   - **Windows:** Descarga desde [git-scm.com](https://git-scm.com/download/win)
   - **Linux:** `sudo apt install git`
   - **Mac:** `brew install git`

3. **Verificar instalación:**
   ```bash
   git --version
   ```

---

## 🚀 Paso a Paso: Crear Repositorio en GitHub

### **1. Crear repositorio en GitHub.com**

1. **Inicia sesión en GitHub**
2. **Menú superior derecha → + → New repository**
3. **Completa los campos:**

   | Campo | Valor |
   |-------|-------|
   | Repository name | `cambus` |
   | Description | `Sistema de Control de Acceso Vehicular - Centro Mabe SLP` |
   | Visibility | `Private` (solo tú) o `Public` (código abierto) |
   | Initialize with README | ❌ No (ya tienes uno) |
   | Add .gitignore | ❌ No (ya tienes uno) |
   | Choose license | Opcional (MIT recomendado) |

4. **Click en "Create repository"**

GitHub te mostrará instructions tipo:

```
…or push an existing repository from the command line
```

Copia esos comandos, los usaremos en el siguiente paso.

---

### **2. Configurar Git (Primera Vez)**

```bash
# Configura tu identidad en Git
git config --global user.name "Tu Nombre Completo"
git config --global user.email "tu.email@gmail.com"

# Verifica la configuración
git config --global --list
```

---

### **3. Inicializar repositorio local**

```bash
# Entra a la carpeta del proyecto
cd /ruta/a/cambus

# Inicializa Git
git init

# Ver estado
git status
```

**Verás algo como:**
```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .env.example
        app.py
        ...
```

---

### **4. Primer Commit**

```bash
# Agregar todos los archivos (respeta .gitignore)
git add .

# Crear primer commit
git commit -m "Initial commit: CamBus v1.0.0 - Sistema de Control Vehicular"

# Ver el commit
git log --oneline
```

---

### **5. Conectar con GitHub (HTTPS)**

```bash
# Cambiar el nombre de rama a 'main' (estándar actual)
git branch -M main

# Agregar el repositorio remoto (reemplaza USERNAME con tu usuario)
git remote add origin https://github.com/USERNAME/cambus.git

# Verificar conexión
git remote -v
```

**Debería mostrar:**
```
origin  https://github.com/USERNAME/cambus.git (fetch)
origin  https://github.com/USERNAME/cambus.git (push)
```

---

### **6. Subir a GitHub**

```bash
# Primera vez: especifica rama con -u
git push -u origin main

# Siguientes: solo git push
```

**Debería pedir credenciales:**
- **Username:** Tu usuario de GitHub
- **Password:** Tu token personal (no contraseña) o contraseña si tienes autenticación básica

---

## 🔐 Alternativa: SSH (Más Seguro)

Si prefieres no ingresar credenciales cada vez, usa SSH:

### **1. Generar clave SSH**

```bash
# En Windows, Mac o Linux
ssh-keygen -t ed25519 -C "tu.email@gmail.com"
# O si falla ed25519:
ssh-keygen -t rsa -b 4096 -C "tu.email@gmail.com"

# Presiona ENTER para todas las preguntas (dejar defaults)
```

Se crearán dos archivos en `~/.ssh/`:
- `id_ed25519` (privada - **NO COMPARTAS**)
- `id_ed25519.pub` (pública - sí la compartas)

### **2. Agregar clave a GitHub**

1. **Copia la clave pública:**
   ```bash
   # En Windows PowerShell:
   Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard
   
   # En Linux/Mac:
   cat ~/.ssh/id_ed25519.pub | pbcopy  # Mac
   cat ~/.ssh/id_ed25519.pub | xclip  # Linux (instala xclip primero)
   ```

2. **Ve a GitHub → Settings → SSH and GPG keys → New SSH key**
   - **Title:** `Mi Computadora` (o el nombre del PC)
   - **Key:** Pega la clave copiada
   - **Add SSH Key**

### **3. Probar conexión SSH**

```bash
ssh -T git@github.com
```

Debería mostrar:
```
Hi USERNAME! You've successfully authenticated...
```

### **4. Cambiar URL de repositorio a SSH**

```bash
# Si ya está configurado HTTPS, cambia a SSH
git remote set-url origin git@github.com:USERNAME/cambus.git

# Verifica
git remote -v
```

---

## 📤 Workflow Normal (Después de Setup)

### **Después de cambios locales:**

#### **Opción 1: Comando Manual**
```bash
# Ver qué cambió
git status

# Agregar cambios
git add .

# Hacer commit con descripción
git commit -m "Agregué feature X"

# Subir a GitHub
git push
```

#### **Opción 2: Script Automatizado** (RECOMENDADO)

```bash
# Windows
push.bat

# Linux/Mac
./push.sh
```

El script automatiza todo, solo te pide el mensaje de commit.

---

## 🔄 Comandos Útiles Git

| Comando | Qué hace |
|---------|----------|
| `git status` | Ver cambios pendientes |
| `git add .` | Preparar todos los cambios |
| `git commit -m "msg"` | Guardar cambios locamente |
| `git push` | Subir a GitHub |
| `git pull` | Descargar cambios desde GitHub |
| `git log --oneline` | Ver historial de commits |
| `git diff` | Ver qué cambió |
| `git reset HEAD~1` | Deshacer último commit |

---

## 💡 Buenas Prácticas

### **Mensajes de Commit Claros**

❌ **Malo:**
```
git commit -m "Fix"
git commit -m "Update files"
```

✅ **Bueno:**
```
git commit -m "Fix: Corregir error de conexión a PostgreSQL"
git commit -m "Feature: Agregar filtro por fecha en reportes"
git commit -m "Docs: Actualizar instrucciones de instalación"
git commit -m "Refactor: Simplificar lógica de autenticación"
```

### **Esquema de Mensajes:**
```
<tipo>: <descripción>

<descripción breve de cambios>
```

**Tipos comunes:**
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `style:` - Formato (no afecta código)
- `refactor:` - Reestructura sin cambio funcional
- `test:` - Agregar/modificar tests
- `chore:` - Tareas de mantenimiento

---

## ⚠️ Qué NO Subir (está en .gitignore)

✅ **Ya está configurado, pero recuerda:**

```
❌ venv/                 # Entorno virtual
❌ __pycache__/          # Caché de Python
❌ .env                  # Credenciales
❌ *.pyc                 # Archivos compilados
❌ .streamlit/           # Caché de Streamlit
```

**Si accidentalmente subiste `.env` con credenciales:**

```bash
# Eliminar del repositorio (pero no localmente)
git rm --cached .env

# Hacer commit de eliminación
git commit -m "Remove: Eliminar .env del repositorio"

# Subir
git push

# IMPORTANTE: Cambiar credenciales en PostgreSQL/servicios
```

---

## 🚸 Errores Comunes

### **Error: "fatal: not a git repository"**
```bash
# Solución: estás fuera de la carpeta del proyecto
cd /ruta/a/cambus
git init  # o git clone si es de un repositorio existente
```

### **Error: "Permission denied (publickey)"**
```bash
# Solución: SSH no está configurado correctamente
# Verifica que la clave SSH está agregada a GitHub:
ssh -T git@github.com
```

### **Error: "failed to push some refs"**
```bash
# Solución: alguien más cambió el repo, sincroniza
git pull
# Resuelve conflictos si los hay
git push
```

---

## 📊 Estructura de Carpeta Perfecta

Después de todo configurado, tu estructura debería verse así:

```
cambus/
├── .git/                 # (Automático) Repositorio Git
├── .gitignore            # ✓ Ya exists
├── setup.bat / setup.sh  # ✓ Ya existen
├── push.bat / push.sh    # ✓ Nuevos, para Git
├── app.py
├── requirements.txt
└── ... otros archivos
```

---

## 🎯 Checklist de Setup Completo

- [ ] Crear repositorio en GitHub
- [ ] Configurar Git localmente (`git config`)
- [ ] Ejecutar `git init` en la carpeta del proyecto
- [ ] Hacer primer commit (`git add . && git commit`)
- [ ] Conectar con GitHub (`git remote add origin`)
- [ ] Hacer primer push (`git push -u origin main`)
- [ ] Probar que `push.bat` o `push.sh` funciona
- [ ] Cambiar contraseña en PostgreSQL (por seguridad)

---

## 📚 Recursos Útiles

- **GitHub Docs:** https://docs.github.com
- **Git Cheat Sheet:** https://git-scm.com/docs
- **Learn Git Interactively:** https://learngitbranching.js.org/
- **Markdown Formatting:** https://guides.github.com/features/mastering-markdown/

---

## 📝 El Archivo README.md en GitHub

Tu `README.md` será la portada del repositorio. Asegúrate que:

✅ Tienes un buen título y descripción  
✅ Instrucciones claras de instalación  
✅ Screenshots o GIFs de la app funcionando  
✅ Estructura de carpetas  
✅ Cómo contribuir (si es open source)  
✅ Licencia

El tuyo ya es muy bueno, solo mantén actualizado.

---

## 🔒 Seguridad

**⚠️ NUNCA SUBAS:**
- `.env` (credenciales)
- `secrets/` (claves privadas)
- Contraseñas en comentarios
- Tokens de API

**Si subiste sin querer:**
```bash
# Cambiar la contraseña inmediatamente en PostgreSQL
# Revocar tokens en servicios usados
# Hacer git rm --cached de archivos sensibles
```

---

**Última actualización:** Marzo 2026  
**Versión:** CamBus 1.0.0
