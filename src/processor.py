import os
import json
from uuid import uuid4, UUID
from typing import List, Dict, Optional, Tuple

from definitions import *
from config import ScoringSystem

class BiwengerProcessor:
    score: int

    def __init__(self, score: int = 1) -> None:
        self.score = score
        self.scoring_folder: str = self._get_scoring_folder(score=score)
        
    def _get_scoring_folder(self, score: int) -> str:
        """
        Devuelve la carpeta del sistema de puntuación a partir de su valor.
        
        Args:
            score (int): Sistema de puntuación.
        
        Returns:
            str: Nombre de la carpeta del sistema de puntuación.
        """
        scoring_system: ScoringSystem = ScoringSystem.from_value(value=score)
        folder: str = scoring_system.get_scoring_system()
        if folder != "Sistema de puntuación desconocido":
            return folder
        else:
            raise ValueError("Sistema de puntuación no soportado.")
        
    def _load_json(self, path: str) -> Dict:
        """
        Carga un archivo JSON y lo convierte en un diccionario.
        
        Args:
            path (str): Ruta del archivo JSON.
        
        Returns:
            dict: Contenido del archivo JSON como diccionario.
        """
        with open(file=path, mode="r", encoding="utf-8") as file:
            data: Dict = json.load(fp=file)
        return data
    
    def _load_game(self, game_name: str, round: int, season: int, score: Optional[int] = None) -> Dict:
        """
        Carga el archivo JSON de un partido específico.
        
        Args:
            game_name (str): Nombre del archivo JSON del partido.
            round (int): Número de la jornada.
            season (int): Año de la temporada.
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        
        Returns:
            dict: Contenido del archivo JSON como diccionario.
        """
        if score is None:
            scoring_folder: str = self.scoring_folder
        else:
            scoring_folder: str = self._get_scoring_folder(score=score)

        path: str = os.path.join("data/JSONs/Games", scoring_folder, str(object=season), f"R{round}", f"{game_name}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo {path} no existe.")
        
        return self._load_json(path=path)
    
    def _load_round(self, round: int, season: int) -> Dict:
        """
        Carga el archivo JSON de una jornada específica.
        
        Args:
            round (int): ID de la jornada.
            season (int): ID de la temporada.
        
        Returns:
            dict: Contenido del archivo JSON como diccionario.
        """
        path: str = os.path.join("data/JSONs/Rounds", str(object=season), f"R{round}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo {path} no existe.")
        
        return self._load_json(path=path)
    
    def _load_season(self, season: int) -> Dict:
        """
        Carga el archivo JSON de una temporada específica.

        Args:
            season (int): ID de la temporada.

        Returns:
            dict: Contenido del archivo JSON como diccionario.
        """
        path: str = os.path.join("data/JSONs/Seasons", f"{season}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo {path} no existe.")
        
        return self._load_json(path=path)
   
    def _get_match(self, match_raw_data: Dict, round_raw_data: Dict) -> Match:
        """
        Procesa un partido específico.
        
        Args:
            game_name (str): Nombre del archivo JSON del partido.
            round (int): Número de la jornada.
            season (int): Año de la temporada.
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        
        Returns:
            Match: Contenido del archivo JSON como objeto.
        """
        return Match(
            match_id=match_raw_data["data"]["id"],
            round_id=round_raw_data["data"]["id"],
            home_team_id=match_raw_data["data"]["home"]["id"],
            away_team_id=match_raw_data["data"]["away"]["id"],
            date=match_raw_data["data"]["date"],
            status=match_raw_data["data"]["status"],
            home_team_score=match_raw_data["data"]["home"]["score"],
            away_team_score=match_raw_data["data"]["away"]["score"]
        )
    
    def _get_player_events(self, player_raw_data: Dict, player_performance_id: UUID) -> List[Event]:
        """
        Procesa los eventos de un jugador en un partido específico.
        
        Args:
            player_raw_data (dict): Datos del jugador.
        
        Returns:
            List[Event]: Eventos del jugador en el partido.
        """
        events: List[Event] = []
        if "events" in player_raw_data:
            for event in player_raw_data["events"]:
                events.append(
                    Event(
                        event_id=event["type"],
                        player_performance_id=player_performance_id,
                        event_metadata=event["metadata"]
                    )
                )
        return events
    
    def _get_player_game(self, player_raw_data: Dict, match_id: int, team_id: int) -> Tuple[PlayerPerformance, List[Event]]:
        """
        Procesa el rendimiento de un jugador en un partido específico.
        
        Args:
            player_raw_data (dict): Datos del partido.
        
        Returns:
            PlayerPerformance: Rendimiento del jugador en el partido.
        """
        players_performance_id: UUID = uuid4()
        events: List[Event] = self._get_player_events(
            player_raw_data=player_raw_data,
            player_performance_id=players_performance_id
        )
        player_performance: PlayerPerformance = PlayerPerformance(
            player_performance_id=players_performance_id,
            player_id=player_raw_data["player"]["id"],
            match_id=match_id,
            team_id=team_id,
            points=player_raw_data["points"]
        )
        return player_performance, events
    
    def _get_players_performance(self, team_raw_data: Dict, match_id: int) -> List[Dict[str, PlayerPerformance | List[Event]]]:
        """
        Procesa el rendimiento de los jugadores de un equipo en un partido específico.
        
        Args:
            team_raw_data (dict): Datos del equipo.
            match_id (int): ID del partido.
        
        Returns:
            List[PlayerPerformance]: Rendimiento de los jugadores en el partido.
        """
        players_performance: List[Dict[str, PlayerPerformance | List[Event]]] = []
        for player_raw_data in team_raw_data["reports"]:
            player_game: Tuple[PlayerPerformance, List[Event]] = self._get_player_game(
                player_raw_data=player_raw_data,
                match_id=match_id,
                team_id=team_raw_data["id"]
            )
            players_performance.append(
                {
                    "player_performance": player_game[0],
                    "events": player_game[1]
                }
            )
        return players_performance
    
    def process_match(self, game_name: str, round: int, season: int, score: Optional[int] = None) -> Match:
        match_raw_data: Dict = self._load_game(game_name=game_name, round=round, season=season, score=score)
        round_raw_data: Dict = self._load_round(round=round, season=season)
        return self._get_match(
            match_raw_data=match_raw_data,
            round_raw_data=round_raw_data
        )
    
    def process_players_performance(self, game_name: str, round: int, season: int, score: Optional[int] = None) -> Dict[str, List[Dict[str, PlayerPerformance | List[Event]]]]:
        """
        Procesa el rendimiento de los jugadores en un partido específico.

        Args:
            game_name (str): Nombre del archivo JSON del partido.
            round (int): Número de la jornada.
            season (int): Año de la temporada.
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.

        Returns:
        """
        match_raw_data: Dict = self._load_game(game_name=game_name, round=round, season=season, score=score)
        match_id: int = match_raw_data["data"]["id"]

        teams_performance: Dict[str, List[Dict[str, PlayerPerformance | List[Event]]]] = {
            "home": self._get_players_performance(
                team_raw_data=match_raw_data["data"]["home"],
                match_id=match_id
            ),
            "away": self._get_players_performance(
                team_raw_data=match_raw_data["data"]["away"],
                match_id=match_id
            )
        }
        return teams_performance
    
    def process_game(self, game_name: str, round: int, season: int, score: Optional[int] = None):
        """
        Procesa un partido específico y devuelve su información.

        Args:
            game_name (str): Nombre del archivo JSON del partido.
            round (int): Número de la jornada.
            season (int): Año de la temporada.
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        """
        match_raw_data: Dict = self._load_game(game_name=game_name, round=round, season=season, score=score)
        round_raw_data: Dict = self._load_round(round=round, season=season)
        
        match: Match = self._get_match(
            match_raw_data=match_raw_data,
            round_raw_data=round_raw_data
        )

        teams_performance: Dict[str, List[Dict[str, PlayerPerformance | List[Event]]]] = {
            "home": self._get_players_performance(
                team_raw_data=match_raw_data["data"]["home"],
                match_id=match.match_id
            ),
            "away": self._get_players_performance(
                team_raw_data=match_raw_data["data"]["away"],
                match_id=match.match_id
            )
        }

if __name__ == "__main__":
    processor = BiwengerProcessor()
    
    game: Match = processor.process_match(game_name="Sevilla vs Valencia", round=1, season=2015)
    print(game)

    players_performance: Dict[str, List[Dict[str, PlayerPerformance | List[Event]]]] = processor.process_players_performance(game_name="Sevilla vs Valencia", round=1, season=2015)
    print(players_performance["home"][0])
    print(players_performance["away"][0])