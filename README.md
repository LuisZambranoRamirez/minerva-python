# Levantar el proyecto

## 1. Crear el entorno virtual

```powershell
python -m venv venv
```

## 2. Activar el entorno virtual

En Windows (PowerShell):

```powershell
.\venv\Scripts\Activate
```

## 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

## 4. Ejecutar el proyecto

```powershell
uvicorn src.main:app --reload
```

## 5. Abrir en el navegador

```text
http://127.0.0.1:8000
```

Documentación automática de FastAPI:

```text
http://127.0.0.1:8000/docs
```

# Mantenimiento de dependencias

Cuando se instale una nueva librería en el proyecto, actualizar el archivo `requirements.txt` ejecutando:

```powershell
pip freeze > requirements.txt
```

Esto guarda todas las dependencias y versiones actuales del entorno virtual para que otros desarrolladores puedan instalar exactamente las mismas versiones.