# 🐍 Guía de Entornos Virtuales en Python

## ¿Qué es un entorno virtual?

Un **entorno virtual** (virtual environment o venv) es un directorio que contiene una instalación aislada de Python con sus propias librerías y dependencias, independiente del sistema Python global.

---

## ¿Por qué usar entornos virtuales?

### 1. **Aislamiento de dependencias**
Cada proyecto puede tener sus propias versiones de librerías sin conflictos.

**Ejemplo del problema sin venv:**
```
Proyecto A necesita: Django 3.2
Proyecto B necesita: Django 4.1
❌ Conflicto: Solo puedes tener una versión instalada globalmente
```

**Con venv:**
```
Proyecto A → venv_a/ → Django 3.2 ✅
Proyecto B → venv_b/ → Django 4.1 ✅
```

### 2. **Reproducibilidad**
Otros desarrolladores pueden recrear exactamente tu entorno usando `requirements.txt`.

### 3. **Limpieza del sistema**
No "contaminas" tu instalación global de Python con dependencias de proyectos específicos.

### 4. **Seguridad**
Reduces el riesgo de conflictos entre versiones que pueden causar errores difíciles de detectar.

---

## Cómo crear y usar un entorno virtual

### Windows

#### 1. Crear el entorno virtual
```bash
python -m venv venv
```

**Explicación:**
- `python`: Ejecuta Python
- `-m venv`: Usa el módulo venv
- `venv`: Nombre del directorio (puedes usar otro nombre)

#### 2. Activar el entorno virtual
```bash
venv\Scripts\activate
```

**Verificar activación:**
Verás `(venv)` al inicio de tu línea de comandos:
```
(venv) C:\Users\Franco\proyecto>
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Trabajar normalmente
Todos los comandos `pip install` y `python` usarán el entorno virtual.

#### 5. Desactivar (cuando termines)
```bash
deactivate
```

---

### Linux / macOS

#### 1. Crear el entorno virtual
```bash
python3 -m venv venv
```

#### 2. Activar el entorno virtual
```bash
source venv/bin/activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Desactivar
```bash
deactivate
```

---

## Estructura del proyecto con venv

```
pp2-soldasur-2c-2025/
├── venv/                    ← Entorno virtual (NO subir a Git)
│   ├── Scripts/             ← Windows
│   ├── bin/                 ← Linux/macOS
│   ├── Lib/
│   └── Include/
├── app/                     ← Código de la aplicación
├── requirements.txt         ← Lista de dependencias
├── .gitignore              ← Debe incluir venv/
└── README.md
```

---

## Archivo requirements.txt

### ¿Qué es?
Un archivo que lista todas las dependencias del proyecto con sus versiones exactas.

### Crear requirements.txt
```bash
# Con el venv activado
pip freeze > requirements.txt
```

### Instalar desde requirements.txt
```bash
pip install -r requirements.txt
```

### Ejemplo de requirements.txt (SOLDASUR):
```
fastapi==0.115.12
uvicorn==0.34.3
ollama==0.6.0
faiss-cpu==1.11.0
sentence-transformers==3.0.1
torch==2.7.1
```

---

## Buenas prácticas

### ✅ HACER:
1. **Crear un venv por proyecto**
2. **Activar el venv antes de trabajar**
3. **Agregar `venv/` al `.gitignore`**
4. **Mantener `requirements.txt` actualizado**
5. **Documentar la versión de Python usada**

### ❌ NO HACER:
1. **Subir `venv/` a Git** (es muy pesado y específico de tu máquina)
2. **Instalar paquetes sin activar el venv**
3. **Compartir el directorio `venv/` entre proyectos**
4. **Usar `sudo pip install` (Linux/macOS)**

---

## Verificar que estás en el venv

### Método 1: Prefijo en terminal
```bash
(venv) C:\Users\Franco\proyecto>  ← El (venv) indica que está activo
```

### Método 2: Comando which/where
**Windows:**
```bash
where python
# Debería mostrar: C:\...\proyecto\venv\Scripts\python.exe
```

**Linux/macOS:**
```bash
which python
# Debería mostrar: /home/.../proyecto/venv/bin/python
```

### Método 3: Verificar paquetes instalados
```bash
pip list
# Solo deberías ver los paquetes del proyecto, no los globales
```

---

## Solución de problemas comunes

### ❌ "pip no se reconoce como comando"

**Causa:** Python no está en el PATH o el venv no está activado.

**Solución:**
```bash
# Windows
python -m pip install <paquete>

# O reinstalar Python marcando "Add to PATH"
```

### ❌ "No se puede activar el venv en Windows"

**Causa:** Política de ejecución de scripts de PowerShell.

**Solución:**
```powershell
# Ejecutar PowerShell como administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego activar normalmente
venv\Scripts\activate
```

### ❌ "ModuleNotFoundError después de activar venv"

**Causa:** El paquete no está instalado en el venv.

**Solución:**
```bash
# Con venv activado
pip install -r requirements.txt
```

### ❌ "El venv ocupa mucho espacio"

**Causa:** Normal, puede ocupar 200MB-2GB según las dependencias.

**Solución:**
- Es normal, no lo subas a Git
- Puedes eliminarlo y recrearlo cuando quieras:
  ```bash
  # Eliminar
  rm -rf venv/  # Linux/macOS
  rmdir /s venv  # Windows
  
  # Recrear
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```

---

## Comandos útiles

```bash
# Ver paquetes instalados
pip list

# Ver paquetes desactualizados
pip list --outdated

# Actualizar un paquete
pip install --upgrade <paquete>

# Desinstalar un paquete
pip uninstall <paquete>

# Ver información de un paquete
pip show <paquete>

# Buscar paquetes
pip search <término>  # (deshabilitado en PyPI)
```

---

## Alternativas a venv

### 1. **virtualenv** (más antiguo, más flexible)
```bash
pip install virtualenv
virtualenv venv
```

### 2. **conda** (para ciencia de datos)
```bash
conda create -n soldasur python=3.11
conda activate soldasur
```

### 3. **pipenv** (combina pip + venv)
```bash
pip install pipenv
pipenv install
pipenv shell
```

### 4. **poetry** (gestión moderna de dependencias)
```bash
pip install poetry
poetry install
poetry shell
```

---

## Para el proyecto SOLDASUR

### Configuración inicial completa:

```bash
# 1. Clonar repositorio
git clone <url-repo>
cd pp2-soldasur-2c-2025

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar (Windows)
venv\Scripts\activate

# 4. Actualizar pip
python -m pip install --upgrade pip

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Verificar instalación
pip list

# 7. Iniciar servidor
python -m uvicorn app.main:app --reload
```

### Workflow diario:

```bash
# Al empezar a trabajar
cd pp2-soldasur-2c-2025
venv\Scripts\activate

# Trabajar normalmente...

# Al terminar
deactivate
```

---

## Resumen ejecutivo

| Acción | Comando Windows | Comando Linux/macOS |
|--------|----------------|---------------------|
| Crear venv | `python -m venv venv` | `python3 -m venv venv` |
| Activar | `venv\Scripts\activate` | `source venv/bin/activate` |
| Desactivar | `deactivate` | `deactivate` |
| Instalar deps | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Guardar deps | `pip freeze > requirements.txt` | `pip freeze > requirements.txt` |

---

## Referencias

- [Documentación oficial de venv](https://docs.python.org/3/library/venv.html)
- [Python Packaging User Guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
- [Real Python - Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)

---

**Última actualización:** Octubre 2025  
**Proyecto:** SOLDASUR 2025 - PP2 2C 2025
