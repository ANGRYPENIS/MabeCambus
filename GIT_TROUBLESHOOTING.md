# 🔧 Git Troubleshooting - CamBus

Soluciones a errores comunes de Git/GitHub.

---

## ❌ Error: "refusing to merge unrelated histories"

### **Síntoma:**
```
fatal: refusing to merge unrelated histories
```

### **Causa:**
Git rechaza hacer merge porque las dos ramas **(local y remota) no tienen un ancestro común**.

Esto pasa típicamente cuando:
1. ✅ Creaste un repo LOCAL con `git init`
2. ✅ Creaste un repo REMOTO en GitHub con archivos iniciales (README, LICENSE)
3. 🔀 Nunca los sincronizaste antes

El historial de commits es completamente diferente en ambas máquinas.

### **Soluciones:**

#### **✅ Opción 1: Permitir Merge de Historiales No Relacionados (RECOMENDADO)**

```bash
# Esto le dice a Git: "confío en que son la misma rama"
git pull origin main --allow-unrelated-histories --no-edit

# Luego push
git push origin main
```

**Esto es exactamente lo que necesitas.** El flag `--allow-unrelated-histories` permite mergear dos ramas con historiales completamente diferentes.

---

#### **✅ Opción 2: Usar el Script (Automático)**

```bash
# Windows
push.bat

# Linux/Mac
./push.sh
```

El script ahora intenta automáticamente con `--allow-unrelated-histories` PRIMERO.

---

### **Por Qué Pasa Esto:**

Cuando hiciste:

```bash
# Local
git init
git add .
git commit -m "Initial commit"

# Luego en GitHub
# Creaste repo CON README/LICENSE/etc
```

Git vio:
- **Local:** Historial que empieza con "Initial commit CamBus..."
- **Remoto:** Historial que empieza con GitHub creando archivos

**Son dos historiales diferentes**, no un descendiente del otro.

---

## ❌ Error: "divergent branches and need to specify how to reconcile them"

### **Síntoma:**
```
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint:
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
fatal: Need to specify how to reconcile divergent branches.
```

### **Causa:**
Las ramas **local** y **remota** tienen historiales completamente diferentes:

1. ✅ Creaste commits locales sin haber hecho `git pull` primero
2. ✅ GitHub tiene archivos que tú no tienes (README, .gitignore, LICENSE)
3. 🔄 Las historias no comparten un ancestro común

### **Soluciones:**

#### **✅ Opción 1: Merge (La más Fácil - RECOMENDADO)**

```bash
# Telling Git to merge las ramas
git pull origin main --no-rebase

# Luego push
git push origin main
```

El `--no-rebase` le dice a Git que haga un merge (combina las historias).

---

#### **✅ Opción 2: Rebase**

```bash
# Reescribir tu historial local encima del remoto
git pull origin main --rebase

# Luego push
git push origin main
```

⚠️ El rebase reescribe tu historial, úsalo solo si no compartiste los commits.

---

#### **✅ Opción 3: Permitir Historiales No Relacionados**

```bash
# Para cuando es la primera vez sincronizando GitHub
git pull origin main --allow-unrelated-histories

# Luego push
git push origin main
```

---

#### **✅ Opción 4: Configurar Globalmente**

```bash
# Establecer default para todos tus repositorios
git config --global pull.rebase false

# Ahora todos los pulls usarán merge por default
git pull origin main
git push origin main
```

---

### **Mi Recomendación para Ti:**

```bash
cd /home/ang/cambus

# Usa el script mejorado que ahora maneja esto automáticamente:
./push.sh  # Linux/Mac
# o
push.bat   # Windows

# O manualmente (lo más directo):
git pull origin main --no-rebase
git push origin main
```

---

## ❌ Error: "non-fast-forward" / "Updates were rejected"

### **Síntoma:**
```
! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ANGRYPENIS/MabeCambus.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart.
```

### **Causa:**
GitHub tiene cambios que tu máquina local **no tiene**. Esto ocurre cuando:

1. ✅ GitHub creó archivos automáticamente (README, LICENSE, .gitignore)
2. 🔄 Alguien más hizo push desde otra máquina
3. 🖥️ Trabajaste desde dos computadoras diferentes

### **Soluciones:**

#### **✅ Opción 1: Pull + Push (RECOMENDADO)**

```bash
# Traer los cambios remotos
git pull origin main

# Subir tu código
git push origin main
```

Si hay conflictos, Git te los mostrará. Resuelve diciendo que aceptes tus cambios locales:

```bash
# Ver conflictos
git status

# Resolver (usar tus cambios)
git add .
git commit -m "Merge: Sincronizar con cambios remotos"
git push
```

---

#### **⚠️ Opción 2: Force Push (SOLO SI ERES SEGURO)**

```bash
# Sobrescribe COMPLETAMENTE lo remoto con tu código local
git push --force origin main
```

**⚠️ PELIGRO:**
- Elimina cambios remotos completamente
- Úsalo solo si eres el único desarrollador
- Si hay otros, pueden perder su trabajo

---

#### **✅ Opción 3: Usar el Script Mejorado**

He actualizado `push.bat` y `push.sh` para manejar esto automáticamente:

```bash
# Windows
push.bat

# Linux/Mac
./push.sh
```

El script intentará:
1. Hacer commit
2. Hacer push
3. Si falla, automáticamente hace `git pull`
4. Intenta push de nuevo

---

## ❌ Error: "Permission denied (publickey)"

### **Síntoma:**
```
Permission denied (publickey).
fatal: Could not read from remote repository.
```

### **Causa:**
Estás usando SSH pero no configuraste las claves correctamente.

### **Soluciones:**

#### **Opción 1: Cambiar a HTTPS (Más Fácil)**

```bash
# Ver URL actual
git remote -v

# Cambiar a HTTPS
git remote set-url origin https://github.com/ANGRYPENIS/MabeCambus.git

# Verifica
git remote -v

# Intenta push
git push
```

Te pedirá username y password (o token personal).

#### **Opción 2: Arreglar SSH**

```bash
# Verificar si la clave está en ssh-agent
ssh-add -l

# Si no ve la clave, agregarla
ssh-add ~/.ssh/id_ed25519
# O si usas RSA:
ssh-add ~/.ssh/id_rsa

# Probar conexión
ssh -T git@github.com

# Si sale "Hi USERNAME!", está bien. Si no, hacer:
ssh-keygen -t ed25519 -C "tu.email@gmail.com"
# Y agregar la nueva clave a GitHub Settings
```

---

## ❌ Error: "fatal: not a git repository"

### **Síntoma:**
```
fatal: not a git repository (or any of the parent directories): .git
```

### **Causa:**
No estás en la carpeta del proyecto o Git no está inicializado.

### **Soluciones:**

```bash
# 1. Verifica que estás en la carpeta correcta
pwd
# Debería mostrar: /home/ang/cambus

# 2. Si no, ve a la carpeta
cd /home/ang/cambus

# 3. Verifica que Git está inicializado
ls -la | grep .git
# Debería mostrar una carpeta .git

# 4. Si no existe .git, inicializar
git init

# 5. Agregar remoto
git remote add origin https://github.com/ANGRYPENIS/MabeCambus.git

# 6. Pull de la rama remota
git pull origin main
```

---

## ❌ Error: "Merge conflict"

### **Síntoma:**
```
CONFLICT (content modified): archivo.py
Automatic merge failed; fix conflicts and then commit the result.
```

### **Causa:**
El mismo archivo fue modificado en dos lugares (local y remoto).

### **Soluciones:**

#### **Opción 1: Aceptar cambios locales (Lo que hiciste)**

```bash
# Ver conflictos
git status

# Resolver usando cambios locales (los tuyos)
git checkout --ours .

# O específico:
git checkout --ours archivo.py

# Agregar resuelto
git add .

# Confirmar merge
git commit -m "Merge: Resolver conflictos, usar cambios locales"
git push
```

#### **Opción 2: Aceptar cambios remotos (Los de GitHub)**

```bash
# Resolver usando cambios remotos
git checkout --theirs .

# O específico:
git checkout --theirs archivo.py

# Agregar resuelto
git add .

# Confirmar merge
git commit -m "Merge: Resolver conflictos, usar cambios remotos"
git push
```

#### **Opción 3: Resolver Manualmente**

1. Abre el archivo en conflicto
2. Verás marcas como:

```python
<<<<<<< HEAD
# Tu código local
=======
# Código remoto
>>>>>>> origin/main
```

3. Edita para mantener lo que quieras
4. Elimina los marcadores (`<<<<<<<`, `=======`, `>>>>>>>`)
5. Guarda
6. `git add .`
7. `git commit -m "Merge: Resolver conflictos manually"`
8. `git push`

---

## ❌ Error: "The file will be replaced by merge"

### **Síntoma:**
```
error: The following untracked working tree files would be overwritten by merge:
    archivo.py
Please move or remove these files before merging.
```

### **Causa:**
Git quiere traer un archivo del remoto pero existe uno local no rastreado.

### **Soluciones:**

```bash
# Opción 1: Eliminar el archivo local (si no lo necesitas)
rm archivo.py
git pull

# Opción 2: Mover el archivo a otra carpeta temporalmente
mv archivo.py archivo.py.backup
git pull
# Luego combina manualmente si necesitas

# Opción 3: Limpiar todo y empezar (NUCLEAR)
git reset --hard HEAD
git pull
```

---

## ❌ Error: "Your branch is ahead of 'origin/main' by X commits"

### **Síntoma:**
```
On branch main
Your branch is ahead of 'origin/main' by 3 commits.
```

### **Causa:**
Hiciste commits locales pero no los subiste a GitHub.

### **Solución:**

```bash
# Simplemente hacer push
git push
```

---

## ❌ Error: "fatal: Credentials could not be converted"

### **Síntoma:**
```
fatal: Credentials could not be converted: windows_crypto_protector=True
```

### **Causa:**
Problema con el gestor de credenciales de Windows.

### **Soluciones:**

```bash
# Opción 1: Usar credenciales sin encriptación
git config --global credential.helper wincred

# Opción 2: Resetear credenciales
# Windows: Ir a Control Panel > Credential Manager
#         Buscar "git:..." y eliminar
#         Luego git push para re-ingresar

# Opción 3: Usar Token Personal
# En GitHub: Settings > Developer settings > Personal access tokens
# Generar token, usarlo como password en git push
```

---

## ✅ Comandos Útiles para Diagnosticar

```bash
# Ver estado actual
git status

# Ver cambios no commiteados
git diff

# Ver cambios por comitear
git diff --staged

# Ver historial de commits
git log --oneline -10

# Ver ramas
git branch -a

# Ver configuración
git config --list

# Ver conexión remota
git remote -v

# Ver último commit
git log -1 --stat
```

---

## 💡 Mejores Prácticas

### **Antes de hacer push:**

```bash
# 1. Ver qué vas a subir
git status
git diff

# 2. Verificar que nadie más hizo cambios
git fetch
git log --oneline -5 origin/main

# 3. Si hay cambios remotos, hacer pull
git pull

# 4. Ahora hacer push
git push
```

### **Configurar Git para la primera vez:**

```bash
# Identidad
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@gmail.com"

# Editor por defecto para commits largos
git config --global core.editor "code"  # Si usas VS Code

# Comportamiento de branches
git config --global pull.rebase false   # Usar merge en lugar de rebase

# Colorear output
git config --global color.ui true
```

---

## 🆘 Si Todo Se Arruina

### **Opción Nuclear: Empezar de Cero**

```bash
# 1. Hacer backup de tu código
cp -r cambus cambus_backup

# 2. Eliminar repositorio Git
rm -rf .git

# 3. Inicializar de nuevo
git init
git add .
git commit -m "Initial commit: CamBus v1.0.0"
git branch -M main

# 4. Conectar con GitHub
git remote add origin https://github.com/ANGRYPENIS/MabeCambus.git

# 5. Force push (SOLO SI ERES SEGURO)
git push --force origin main
```

**⚠️ Advertencia:** Esto elimina TODOS los commits anteriores.

---

## 📚 Recursos Útiles

- **GitHub Docs:** https://docs.github.com/pull-requests
- **Git Docs:** https://git-scm.com/doc
- **Git Visualizer:** https://learngitbranching.js.org/
- **Resolving Conflicts:** https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts

---

## 🎯 Para Tu Caso Específico

**Ejecuta esto AHORA para resolver tu error:**

```bash
cd /home/ang/cambus

# Opción 1: Automático (Mi recomendación)
./push.sh  # Linux/Mac
# o
push.bat   # Windows

# Opción 2: Manual
git pull origin main --no-edit
git push origin main
```

El script ahora maneja esto automáticamente.

---

**Última actualización:** Marzo 2026  
**Versión:** CamBus 1.0.0
