

````markdown
# 🧪 Proyecto Autolog - Ingeniería y Calidad de Software - UNT FRD 2025

---

## ⚙️ Configuración inicial del entorno (Django + entorno virtual)

### 📁 1. Crear carpeta del proyecto y entrar

```bash
mkdir autolog-backend
cd autolog-backend
````

🔹 Crea la carpeta raíz del backend y entra a ella.

---

### ✅ 2. Crear el entorno virtual

```bash
python -m venv venv
```

🔹 Crea una carpeta `venv` con un entorno Python aislado para este proyecto.

---

### 🧠 3. Activar el entorno virtual

#### En terminal de Windows (CMD o PowerShell):

```bash
venv\Scripts\activate
```

🔹 Cambia el entorno activo para que `pip` y `python` usen este entorno virtual.

---

### 🧠 4. Usar el entorno virtual desde Visual Studio Code

1. Presionar `F1`
2. Escribir: `Python: Select Interpreter`
3. Elegir la opción que diga algo como:

```
.\venv\Scripts\python.exe
```

🔹 Así, cada vez que abras una terminal nueva en VSCode, usará automáticamente el entorno virtual.

---

### 🛠 5. Instalar Django

```bash
pip install django
```

🔹 Instala el framework Django dentro del entorno virtual.

---

### 🚀 6. Crear el proyecto Django

```bash
django-admin startproject autolog .
```

🔹 El `.` al final indica que el proyecto se cree **dentro de la carpeta actual**, sin generar una subcarpeta duplicada.

---

### 📝 7. Guardar las dependencias del entorno virtual

```bash
pip freeze > requirements.txt
```

🔹 Crea o actualiza el archivo `requirements.txt` con todas las dependencias instaladas.

---

### 🤝 8. Compartir dependencias con el equipo

Cada vez que hacés `git pull` o se actualiza `requirements.txt`, corré:

```bash
pip install -r requirements.txt
```

🔹 Instala todas las dependencias necesarias del proyecto en tu entorno.

---

### ❌ 9. Desactivar el entorno virtual

```bash
deactivate
```

🔹 Vuelve a usar el entorno Python global del sistema.

---

### 🛑 10. Ignorar `venv/` en Git

Asegurate de que tu archivo `.gitignore` contenga:

```
venv/
```

🔹 Así evitamos subir archivos del entorno virtual, ya que es exclusivo de cada máquina y no debe ir al repositorio.

```
