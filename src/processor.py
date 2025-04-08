import os
import json
from uuid import uuid4, UUID
from typing import List, Dict, Optional, Tuple

from definitions import *
from config import ScoringSystem
from src.definitions.event import Event
from src.definitions.player import PlayerPerformance

class BiwengerProcessor:
    score: int

    def __init__(self, score: int = 1) -> None:
        self.score = score
        self.scoring_folder: str = self._get_scoring_folder(score=self.score)

    def set_scoring_system(self, score: int) -> None:
        """
        Cambia el sistema de puntuación a utilizar.
        
        Args:
            score (int): Sistema de puntuación a utilizar.
        """
        self.scoring_folder: str = self._get_scoring_folder(score=score)
        self.score = score
        
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
   
    def _get_season(self, season: int) -> Season:
        """
        Procesa una temporada específica y devuelve su información.

        Args:
            season (int): ID de la temporada.

        Returns:
            Season: Información de la temporada.
        """
        season_raw_data: Dict = self._load_season(season=season)
        
        is_finished: bool = True
        for round_raw_data in season_raw_data["data"]["rounds"]:
            if round_raw_data["status"] != "finished" and round_raw_data["start"] != 0:
                is_finished = False
                break

        return Season(
            season_id=season_raw_data["data"]["id"],
            season_name=season_raw_data["data"]["name"],
            season_status="finished" if is_finished else "in_progress",
        )
    
    def get_seasons(self) -> List[Season]:
        """
        Devuelve una lista con todas las temporadas disponibles.

        Returns:
            List[Season]: Lista de temporadas.
        """
        seasons: List[Season] = []
        for file in os.listdir(path="data/JSONs/Seasons"):
            if file.endswith(".json"):
                season_id: int = int(file.split(sep=".")[0])
                seasons.append(self._get_season(season=season_id))
        return seasons
    
    def _get_round(self, round: int, season: int) -> Round:
        """
        Procesa una jornada específica y devuelve su información.

        Args:
            round (int): ID de la jornada.
            season (int): ID de la temporada.

        Returns:
            Round: Información de la jornada.
        """
        round_raw_data: Dict = self._load_round(round=round, season=season)
        
        round_status: str = round_raw_data["data"]["status"]
        if round_status != "finished":
            for match_raw_data in round_raw_data["data"]["games"]:
                if match_raw_data["status"] == "in_progress":
                    round_status = "in_progress"
                    break
                elif match_raw_data["status"] == "pending":
                    round_status = "pending"

        return Round(
            round_id=round_raw_data["data"]["id"],
            season_id=season,
            name=round_raw_data["data"]["name"],
            status=round_status
        )
    
    def _get_season_rounds(self, season: int) -> List[Round]:
        """
        Devuelve una lista con todas las jornadas de una temporada específica.

        Args:
            season (int): ID de la temporada.

        Returns:
            List[Round]: Lista de jornadas.
        """
        rounds: List[Round] = []
        for file in os.listdir(path=os.path.join("data/JSONs/Rounds", str(object=season))):
            if file.endswith(".json"):
                round_id: int = int(file.split(sep=".")[0][1:])
                rounds.append(self._get_round(round=round_id, season=season))
        return rounds
    
    def get_rounds(self) -> List[Round]:
        """
        Devuelve una lista con todas las jornadas disponibles.

        Returns:
            List[Round]: Lista de jornadas.
        """
        rounds: List[Round] = []
        for season in os.listdir(path="data/JSONs/Rounds"):
            if os.path.isdir(s=os.path.join("data/JSONs/Rounds", season)):
                season_id: int = int(season)
                rounds.extend(self._get_season_rounds(season=season_id))
        return rounds
    
    def _get_game(self, game_name: str, round: int, season: int) -> Game:
        """
        Procesa un partido específico.
        
        Args:
            game_name (str): Nombre del archivo JSON del partido.
            round (int): Número de la jornada.
            season (int): Año de la temporada.
        
        Returns:
            Match: Contenido del archivo JSON como objeto.
        """
        game_raw_data: Dict = self._load_game(game_name=game_name, round=round, season=season, score=self.score)
        round_raw_data: Dict = self._load_round(round=round, season=season)
    
        return Game(
            game_id=game_raw_data["data"]["id"],
            round_id=round_raw_data["data"]["id"],
            home_team_id=game_raw_data["data"]["home"]["id"],
            away_team_id=game_raw_data["data"]["away"]["id"],
            date=game_raw_data["data"]["date"],
            status=game_raw_data["data"]["status"],
            home_team_score=game_raw_data["data"]["home"]["score"],
            away_team_score=game_raw_data["data"]["away"]["score"]
        )
    
    def _get_round_games(self, round: int, season: int) -> List[Game]:
        """
        Devuelve una lista con todos los partidos de una jornada específica.

        Args:
            round (int): ID de la jornada.
            season (int): ID de la temporada.

        Returns:
            List[Game]: Lista de partidos.
        """
        games: List[Game] = []
        for game_name in os.listdir(path=os.path.join("data/JSONs/Games", self.scoring_folder, str(object=season), f"R{round}")):
            if game_name.endswith(".json"):
                game_name: str = game_name[:-5]
                games.append(self._get_game(game_name=game_name, round=round, season=season))
        
        return games
    
    def _get_season_games(self, season: int) -> List[Game]:
        """
        Devuelve una lista con todos los partidos de una temporada específica.

        Args:
            season (int): ID de la temporada.

        Returns:
            List[Game]: Lista de partidos.
        """
        games: List[Game] = []
        for round in os.listdir(path=os.path.join("data/JSONs/Games", self.scoring_folder, str(object=season))):
            if os.path.isdir(s=os.path.join("data/JSONs/Games", self.scoring_folder, str(object=season), round)):
                games.extend(self._get_round_games(round=int(round[1:]), season=season))
        
        return games
    
    def get_games(self) -> List[Game]:
        """
        Devuelve una lista con todos los partidos disponibles.

        Returns:
            List[Game]: Lista de partidos.
        """
        games: List[Game] = []
        for season in os.listdir(path=os.path.join("data/JSONs/Games", self.scoring_folder)):
            if os.path.isdir(s=os.path.join("data/JSONs/Games", self.scoring_folder, season)):
                season_id: int = int(season)
                games.extend(self._get_season_games(season=season_id))

        return games
    
    def _get_player_events(self, events_raw_data: List[Dict], player_performance_id: UUID) -> List[Event]:
        """
        Procesa los eventos de un jugador en un partido específico.
        
        Args:
            events_raw_data (list): Eventos del jugador.
            player_performance_id (UUID): ID de la actuación del jugador.
        
        Returns:
            List[Event]: Eventos del jugador en el partido.
        """
        events: List[Event] = []
        for event in events_raw_data:
            events.append(
                Event(
                    event_type=event["type"],
                    player_performance_id=player_performance_id,
                    event_minute=event["metadata"]
                )
            )
        return events
    
    def _get_player_game(self, player_raw_data: Dict, team_id: int, game_id: int) -> Tuple[PlayerPerformance, List[Event]]:
        """
        Procesa el rendimiento de un jugador en un partido específico.
        
        Args:
            player_raw_data (dict): Datos del jugador.
            team_id (int): ID del equipo.
            game_id (int): ID del partido.
        
        Returns:
            PlayerPerformance: Rendimiento del jugador en el partido.
            List[Event]: Eventos del jugador en el partido.
        """
        player_performance_id: UUID = uuid4()
        
        player_events: List[Event] = self._get_player_events(
            events_raw_data=player_raw_data["events"],
            player_performance_id=player_performance_id
        ) if "events" in player_raw_data else []

        player_performance: PlayerPerformance = PlayerPerformance(
            player_performance_id=player_performance_id,
            player_id=player_raw_data["player"]["id"],
            game_id=game_id,
            team_id=team_id,
            points=player_raw_data["points"]
        )

        return player_performance, player_events
    
    def _get_game_performances(self, game_name: str, round: int, season: int, score: Optional[int] = None) -> Tuple[List[PlayerPerformance], List[Event]]:
        """
        Procesa las actuaciones de los jugadores en un partido específico.
        
        Args:
            game_name (str): Nombre del archivo JSON del partido.
            round (int): Número de la jornada.
            season (int): Año de la temporada.
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        
        Returns:
            Tuple[List[PlayerPerformance], List[Event]]: Actuaciones de los jugadores y eventos del partido.
        """
        game_raw_data: Dict = self._load_game(game_name=game_name, round=round, season=season, score=score)
        
        player_performances: List[PlayerPerformance] = []
        events: List[Event] = []
        
        for team in ["home", "away"]:
            for player_raw_data in game_raw_data["data"][team]["reports"]:
                player_game: Tuple[PlayerPerformance , List[Event]] = self._get_player_game(
                    player_raw_data=player_raw_data,
                    team_id=game_raw_data["data"][team]["id"],
                    game_id=game_raw_data["data"]["id"]
                )
                
                player_performance: PlayerPerformance = player_game[0]
                player_events: List[Event] = player_game[1]
                
                player_performances.append(player_performance)
                events.extend(player_events)

        return player_performances, events
    
    def _get_round_performances(self, round: int, season: int, score: Optional[int] = None) -> Tuple[List[PlayerPerformance], List[Event]]:
        """
        Procesa las actuaciones de los jugadores en una jornada específica.
        
        Args:
            round (int): ID de la jornada.
            season (int): ID de la temporada.
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        
        Returns:
            Tuple[List[PlayerPerformance], List[Event]]: Actuaciones de los jugadores y eventos de la jornada.
        """
        pass

    def _get_season_performances(self, season: int, score: Optional[int] = None) -> Tuple[List[PlayerPerformance], List[Event]]:
        """
        Procesa las actuaciones de los jugadores en una temporada específica.
        
        Args:
            season (int): ID de la temporada.
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        
        Returns:
            Tuple[List[PlayerPerformance], List[Event]]: Actuaciones de los jugadores y eventos de la temporada.
        """
        pass

    def get_performances(self, score: Optional[int] = None) -> Tuple[List[PlayerPerformance], List[Event]]:
        """
        Devuelve las actuaciones de los jugadores y eventos de la temporada actual.
        
        Args:
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        
        Returns:
            Tuple[List[PlayerPerformance], List[Event]]: Actuaciones de los jugadores y eventos de la temporada.
        """
        pass


if __name__ == "__main__":
    processor = BiwengerProcessor()
    
    #game: Match = processor.process_match(game_name="Sevilla vs Valencia", round=1, season=2015)
    #print(game)

    #players_performance: Dict[str, List[Dict[str, PlayerPerformance | List[Event]]]] = processor.process_players_performance(game_name="Sevilla vs Valencia", round=1, season=2015)
    #print(players_performance["home"][0])
    #print(players_performance["away"][0])

    #for season in processor.get_seasons():
    #    print(season)

    #for round in processor._get_season_rounds(season=2015):
    #    print(round)