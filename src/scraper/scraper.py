import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional

from src.utils import wait
from src.definitions import ScoringSystemType
from src.scraper.wrapper import GameDataExtractor
from src.config import Credentials

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BiwengerScraper:
    def __init__(self, credentials: Credentials) -> None:
        self.email: str = credentials.email
        self.password: str = credentials.password
        self.GameDataExtractor: GameDataExtractor = GameDataExtractor(email=self.email, password=self.password)

    def _get_score_folder(self, score: int) -> str:
        """
        Devuelve el nombre de la carpeta donde se guardarán los datos de la temporada.

        Args:
            score (int): Sistema de puntuación.
        """
        scoring_system: ScoringSystemType = ScoringSystemType.from_value(value=score)
        folder: str = scoring_system.get_scoring_system()
        if folder != "Sistema de puntuación desconocido":
            return folder
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
        
    def _get_season_json(self, year: int) -> Dict:
        """
        Obtiene los datos de la temporada 'year' en formato JSON.
        
        Args:
            year (int): Año de la temporada.
            score (int): Sistema de puntuación a utilizar.
        """
        return self.GameDataExtractor.get_season_data(year=year)
    
    def _get_round_json(self, round: Optional[int]) -> Dict:
        """
        Obtiene los datos de la jornada 'round' en formato JSON.
        
        Args:
            round (int): Número de la jornada.
        """
        return self.GameDataExtractor.get_round_data(round=round)
    
    def _get_game_json(self, game: int, score: int) -> Dict:
        """
        Obtiene los datos del partido 'game' en formato JSON.
        
        Args:
            game (int): ID del partido.
            score (int): Sistema de puntuación a utilizar.
        """
        return self.GameDataExtractor.get_game_data(game=game, score=score)

    def save_seasons_data(self) -> None:
        """
        Guarda los datos de las temporadas en formato JSON.

        Args:
            score (int): Sistema de puntuación a utilizar
        """
        if not os.path.exists("data/JSONs/Seasons"):
                os.makedirs(name="data/JSONs/Seasons")

        logging.info(msg=f"Guardando datos de las temporadas en 'data/JSONs/Seasons'...")
        for year in range(2015, datetime.now().year + 1):
            season_data: Dict = self._get_season_json(year=year)

            season_path: str = f"data/JSONs/Seasons/{year}.json"
            if os.path.exists(season_path) and self._is_valid_json(path=season_path):
                logging.info(msg=f"\t\t-Datos de la temporada {year} ya guardados. Continuando...")
                continue
            
            logging.info(msg=f"\t-Guardando datos de la temporada {year}...")
            with open(file=season_path, mode="w", encoding="utf-8") as file:
                json.dump(
                    obj=season_data,
                    fp=file,
                    indent=4,
                    ensure_ascii=False
                )

            logging.info(msg=f"\t-Datos de la temporada {year} guardados correctamente.")
            #wait()

    def save_rounds_data(self) -> None:
        """
        Guarda los datos de las jornadas en formato JSON.

        Args:
            score (int): Sistema de puntuación a utilizar
        """
        logging.info(msg=f"Guardando datos de las jornadas en 'data/JSONs/Rounds'...")
        for season in os.listdir(path=f"data/JSONs/Seasons"):
            season: str = season.split(sep=".")[0]

            if not os.path.exists(f"data/JSONs/Rounds/{season}"):
                os.makedirs(name=f"data/JSONs/Rounds/{season}")

            with open(file=f"data/JSONs/Seasons/{season}.json", mode="r", encoding="utf-8") as file:
                season_data: Dict = json.load(fp=file)
            
            logging.info(msg=f"\t-Guardando datos de las jornadas de la temporada {season}...")
            for round in season_data["data"]["rounds"]:
                round_id: int = round["id"]
                round_name: str = round["short"]

                round_path: str = f"data/JSONs/Rounds/{season}/{round_name}.json"
                if os.path.exists(round_path) and self._is_valid_json(path=round_path):
                    logging.info(msg=f"\t\t-Datos de la jornada {round_name} ya guardados. Continuando...")
                    continue

                logging.info(msg=f"\t\t-Guardando datos de la jornada {round_name}...")
                round_data: Dict = self._get_round_json(round=round_id)
                with open(file=f"data/JSONs/Rounds/{season}/{round_name}.json", mode="w", encoding="utf-8") as file:
                    json.dump(
                        obj=round_data,
                        fp=file,
                        indent=4,
                        ensure_ascii=False
                    )

                logging.info(msg=f"\t\t-Datos de la jornada {round_name} guardados correctamente.")
                #wait()

    def save_games_data(self, score: int = ScoringSystemType.PICAS.value) -> None:
        """
        Guarda los datos de los partidos en formato JSON.

        Args:
            score (int): Sistema de puntuación a utilizar
        """
        score_folder: str = self._get_score_folder(score=score)
        logging.info(msg=f"Guardando datos de los partidos en 'data/JSONs/Games/{score_folder}'...")

        round_folder: str = f"data/JSONs/Rounds"
        for season in os.listdir(path=round_folder):
            logging.info(msg=f"\t-Guardando datos de los partidos de la temporada {season}...")
            for round in os.listdir(path=f"{round_folder}/{season}"):
                round: str = round.split(sep=".")[0]

                if not os.path.exists(f"data/JSONs/Games/{score_folder}/{season}/{round}"):
                    os.makedirs(name=f"data/JSONs/Games/{score_folder}/{season}/{round}")

                with open(file=f"{round_folder}/{season}/{round}.json", mode="r", encoding="utf-8") as file:
                    round_data: Dict = json.load(fp=file)

                logging.info(msg=f"\t\t-Guardando datos de los partidos de la jornada {round}...")
                for game in round_data["data"]["games"]:
                    game_id: int = game["id"]
                    game_name: str = game["home"]["name"] + " vs " + game["away"]["name"]

                    game_path: str = f"data/JSONs/Games/{score_folder}/{season}/{round}/{game_name}.json"
                    if os.path.exists(game_path) and self._is_valid_json(path=game_path):
                        #logging.info(msg=f"\t\t\t-Datos del partido {game_name} ya guardados. Continuando...")
                        continue

                    logging.info(msg=f"\t\t\t-Guardando datos del partido {game_name}...")
                    game_data: Dict = self._get_game_json(game=game_id, score=score)
                    with open(file=f"data/JSONs/Games/{score_folder}/{season}/{round}/{game_name}.json", mode="w", encoding="utf-8") as file:
                        json.dump(
                            obj=game_data,
                            fp=file,
                            indent=4,
                            ensure_ascii=False
                        )

                    logging.info(msg=f"\t\t\t-Datos del partido {game_name} guardados correctamente.")
                    #wait()


if __name__ == "__main__":
    my_credentials: Credentials = Credentials()
    scoring_system: ScoringSystemType = ScoringSystemType.SOFASCORE
    
    scraper: BiwengerScraper = BiwengerScraper(credentials=my_credentials)
    
    #scraper.save_seasons_data()
    #scraper.save_rounds_data()
    scraper.save_games_data(score=scoring_system.get_value())