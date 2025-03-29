# Biwenger Project

## Descripción
Este proyecto tiene como objetivo construir un agente inteligente para gestionar y analizar datos de Biwenger, la liga fantasy del diario AS. La idea es utilizar Python para acceder a la API interna (y, si es necesario, realizar scraping) con el fin de extraer datos como estadísticas de jugadores, puntuaciones por jornada, valores de mercado y resultados de partidos, tanto de la temporada actual como de temporadas anteriores.

## Objetivos
- Automatizar la extracción de datos de Biwenger.
- Almacenar y procesar información histórica de al menos 5 temporadas.
- Desarrollar un motor de recomendaciones que ayude a tomar decisiones de fichajes, ventas y alineaciones.

## Estructura del Proyecto
biwenger_project/
├── biwenger_env/ # Entorno virtual de Python
├── src/ # Código fuente del proyecto
│ ├── init.py
│ ├── auth.py # Módulo de autenticación y manejo de tokens
│ ├── api.py # Módulo para interactuar con la API interna de Biwenger
│ ├── scraper.py # (Opcional) Módulo para scraping web con Selenium/BeautifulSoup
│ └── utils.py # Funciones de utilidad y procesamiento de datos
├── data/ # Datos extraídos (JSON, CSV, etc.)
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo

## Instalación
1. **Clonar el repositorio:**
```bash
git clone https://github.com/mutiel-ds/Biwenger.git
cd Biwenger
```

2. **Crear y activar el entorno virtual:**
En Linux/MacOS:
```bash
python -m venv .venv
source .venv/bin/activate
```
En Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## Uso
- Configura tus credenciales y parámetros necesarios en el módulo auth.py.
- Ejecuta los scripts para autenticarte y extraer datos, por ejemplo:
```bash
python src/auth.py
python src/api.py
```
- Revisa la carpeta data/ para ver la información extraída.