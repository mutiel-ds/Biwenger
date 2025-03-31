# Biwenger Project

## Descripción
Este proyecto tiene como objetivo construir un agente inteligente para gestionar y analizar datos de Biwenger, la liga fantasy del diario AS. La idea es utilizar Python para acceder a la API interna (y, si es necesario, realizar scraping) con el fin de extraer datos como estadísticas de jugadores, puntuaciones por jornada, valores de mercado y resultados de partidos, tanto de la temporada actual como de temporadas anteriores.

## Objetivos
- Automatizar la extracción de datos de Biwenger.
- Almacenar y procesar información histórica de al menos 5 temporadas.
- Desarrollar un motor de recomendaciones que ayude a tomar decisiones de fichajes, ventas y alineaciones.

## Estructura del Proyecto
biwenger_project/
├── src/ # Código fuente del proyecto
│ ├── init.py
│ ├── config.py # Configuración y constantes
│ ├── wrapper.py # Wrapper para la API de Biwenger
│ └── api.py # API customizada del Biwenger
├── data/ # Datos extraídos (JSON, CSV, etc.)
└── requirements.txt # Dependencias del proyecto

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

4. **Configurar variables de entorno:**

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
```
BIWENGER_EMAIL=tu_email
BIWENGER_PASSWORD=tu_password
X-USER=tu_user_id
X-LEAGUE=tu_league_id
X-VERSION=version_api
```

## Uso
1. Asegúrate de tener las variables de entorno configuradas correctamente.
2. Ejecuta los scripts para extraer datos.
3. Los datos extraídos se guardarán en la carpeta `data/` organizados por sistema de puntuación y temporada.

## Sistemas de Puntuación
- PICAS (1): Sistema de puntuación principal de Biwenger
- SOFASCORE (2): Sistema basado en Sofascore
- MEDIA (5): Sistema basado en la media de puntuaciones