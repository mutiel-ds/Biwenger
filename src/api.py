import os
import time
import json
import logging
from datetime import datetime
from typing import Dict, Optional

from wrapper import Extractor

from config import PICAS, SOFASCORE, MEDIA
from config import BIWENGER_EMAIL, BIWENGER_PASSWORD

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BiwengerAPI:
    def __init__(self, email: str, password: str) -> None:
        self.email: str = email
        self.password: str = password
        self.extractor: Extractor = Extractor(email=self.email, password=self.password)

    def _get_score_folder(self, score: int) -> str:
        """
        Devuelve el nombre de la carpeta donde se guardarán los datos de la temporada.

        Args:
            score (int): Sistema de puntuación.
        """
        if score == PICAS:
            return "Picas"
        elif score == SOFASCORE:
            return "SofaScore"
        elif score == MEDIA:
            return "Media"
        else:
            raise ValueError("Sistema de puntuación no soportado.")
        
    def _is_valid_json(self, path: str) -> bool:
        """
        Comprueba si un archivo JSON es válido.

        Args:
            path (str): Ruta del archivo JSON.
        """
        try:
            with open(file=path, mode="r", encoding="utf-8") as file:
                data: Dict = json.load(fp=file)
                return (
                    isinstance(data, dict)
                    and "status" in data
                    and data["status"] == 200
                    and "data" in data
                    and data["data"] is not None
                )
        except (json.JSONDecodeError, FileNotFoundError):
            return False
        
    def _get_season_json(self, year: int, score: int) -> Dict:
        """
        Obtiene los datos de la temporada 'year' en formato JSON.
        
        Args:
            year (int): Año de la temporada.
            score (int): Sistema de puntuación a utilizar.
        """
        return self.extractor.get_season_data(year=year, score=score)
    
    def _get_round_json(self, round: Optional[int]) -> Dict:
        """
        Obtiene los datos de la jornada 'round' en formato JSON.
        
        Args:
            round (int): Número de la jornada.
        """
        return self.extractor.get_round_data(round=round)

    def save_seasons_data(self, score: int = PICAS) -> None:
        """
        Guarda los datos de las temporadas en formato JSON.

        Args:
            score (int): Sistema de puntuación a utilizar
        """
        score_folder: str = self._get_score_folder(score=score)
        logging.info(msg=f"Guardando datos de las temporadas en 'data/{score_folder}/Seasons'...")
        
        for year in range(2015, datetime.now().year + 1):
            season_data: Dict = self._get_season_json(year=year, score=score)
            
            logging.info(msg=f"\t-Guardando datos de la temporada {year}...")
            with open(file=f"data/{score_folder}/Seasons/{year}.json", mode="w", encoding="utf-8") as file:
                json.dump(
                    obj=season_data,
                    fp=file,
                    indent=4,
                    ensure_ascii=False
                )

            logging.info(msg=f"\t-Datos de la temporada {year} guardados correctamente.")
            time.sleep(2)

    def save_rounds_data(self, score: int = PICAS) -> None:
        """
        Guarda los datos de las jornadas en formato JSON.

        Args:
            score (int): Sistema de puntuación a utilizar
        """
        score_folder: str = self._get_score_folder(score=score)
        logging.info(msg=f"Guardando datos de las jornadas en 'data/{score_folder}/Rounds'...")

        for season in os.listdir(path=f"data/{score_folder}/Seasons"):
            season: str = season.split(sep=".")[0]

            if not os.path.exists(f"data/{score_folder}/Rounds/{season}"):
                os.makedirs(name=f"data/{score_folder}/Rounds/{season}")

            with open(file=f"data/{score_folder}/Seasons/{season}.json", mode="r", encoding="utf-8") as file:
                season_data: Dict = json.load(fp=file)
            
            logging.info(msg=f"\t-Guardando datos de las jornadas de la temporada {season}...")
            for round in season_data["data"]["rounds"]:
                round_id: int = round["id"]
                round_name: str = round["short"]

                round_path: str = f"data/{score_folder}/Rounds/{season}/{round_name}.json"
                if os.path.exists(round_path) and self._is_valid_json(path=round_path):
                    logging.info(msg=f"\t\t-Datos de la jornada {round_name} ya guardados. Continuando...")
                    continue

                logging.info(msg=f"\t\t-Guardando datos de la jornada {round_name}...")
                round_data: Dict = self._get_round_json(round=round_id)
                with open(file=f"data/{score_folder}/Rounds/{season}/{round_name}.json", mode="w", encoding="utf-8") as file:
                    json.dump(
                        obj=round_data,
                        fp=file,
                        indent=4,
                        ensure_ascii=False
                    )

                logging.info(msg=f"\t\t-Datos de la jornada {round_name} guardados correctamente.")
                time.sleep(2)

if __name__ == "__main__":
    api: BiwengerAPI = BiwengerAPI(email=BIWENGER_EMAIL, password=BIWENGER_PASSWORD)
    api.save_rounds_data(score=SOFASCORE)