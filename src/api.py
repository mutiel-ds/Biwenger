import logging

import requests
from requests import Response

import json
from typing import Dict

from auth import login
from config import COMPETITION_URL, USER_AGENT
from config import BIWENGER_EMAIL, BIWENGER_PASSWORD

# Configuración de logging (si aún no está configurado en otro módulo)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_competition_data(token: str) -> Dict | None:
    """
    Consulta datos de la competición (ej. La Liga) usando la API interna de Biwenger.
    Retorna el JSON con los datos o None en caso de error.
    """
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT
    }
    
    try:
        response: Response = requests.get(url=COMPETITION_URL, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(msg=f"Error al obtener datos de la competición: {e}")
        return None

    try:
        data: Dict = response.json()
    except ValueError as e:
        logging.error(msg=f"Error al parsear la respuesta JSON de la competición: {e}")
        return None

    logging.info(msg="Datos de competición obtenidos exitosamente.")
    return data

if __name__ == "__main__":
    token: str | None = login(email=BIWENGER_EMAIL, password=BIWENGER_PASSWORD)
    if token:
        competition_data: Dict | None = get_competition_data(token=token)
        if competition_data:
            with open(file="data/competition_data.json", mode="w", encoding="utf-8") as f:
                json.dump(obj=competition_data, fp=f, indent=4, ensure_ascii=False)
            print("Datos de la competición guardados en 'data/competition_data.json'.")
        else:
            print("Error en la obtención de datos de la competición.")
    else:
        print("Fallo en la autenticación, no se puede obtener datos.")
