import os
import json
from uuid import uuid4, UUID
from datetime import datetime
from pydantic import ValidationError
from typing import List, Dict, Optional, Tuple

from src.config import Credentials
from src.scraper.scraper import BiwengerScraper
from src.definitions import (
    Season,
    Round, 
    Game, 
    PlayerPerformance, 
    Event, 
    Player,
    Team, 
    ScoringSystemType,
    PerformanceScore
)

class BiwengerJSONProcessor:
    score: int
    scoring_folder: str
    scraper: BiwengerScraper

    def __init__(self, score: int = 1) -> None:
        self.score = score
        self.scoring_folder: str = self._get_scoring_folder(score=self.score)
        self.scraper: BiwengerScraper = BiwengerScraper(credentials=Credentials())

    def _get_scoring_folder(self, score: int) -> str:
        """
        Devuelve la carpeta del sistema de puntuación a partir de su valor.
        
        Args:
            score (int): Sistema de puntuación.
        
        Returns:
            str: Nombre de la carpeta del sistema de puntuación.
        """
        scoring_system: ScoringSystemType = ScoringSystemType.from_value(value=score)
        folder: str = scoring_system.get_scoring_system()
        if folder != "Sistema de puntuación desconocido":
            return folder
        else:
            raise ValueError("Sistema de puntuación no soportado.")
        
    def set_scoring_system(self, score: int) -> None:
        """
        Cambia el sistema de puntuación a utilizar.
        
        Args:
            score (int): Sistema de puntuación a utilizar.
        """
        self.scoring_folder: str = self._get_scoring_folder(score=score)
        self.score = score
        
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
            round_name=round_raw_data["data"]["name"],
            round_status=round_status
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
    
    def _get_game(self, game_name: str, round: int, season: int) -> Game:
        """
        Procesa un partido específico.
        
        Args:
            game_name (str): Nombre del archivo JSON del partido.
            round (int): Número de la jornada.
            season (int): Año de la temporada.
        
        Returns:
            Game: Contenido del archivo JSON como objeto.
        """
        game_raw_data: Dict = self._load_game(game_name=game_name, round=round, season=season, score=self.score)
        round_raw_data: Dict = self._load_round(round=round, season=season)
    
        if game_raw_data["data"]["status"] == "pending":
            home_team_score: int = -1
            away_team_score: int = -1
        
        elif game_raw_data["data"]["status"] == "preview":
            game_raw_data: Dict = self.scraper._get_game_json(
                game=game_raw_data["data"]["id"],
                score=self.score
            )
            home_team_score: int = game_raw_data["data"]["home"]["score"]
            away_team_score: int = game_raw_data["data"]["away"]["score"]
        
        else:
            home_team_score: int = game_raw_data["data"]["home"]["score"]
            away_team_score: int = game_raw_data["data"]["away"]["score"]

        try:
            game: Game = Game(
                game_id=game_raw_data["data"]["id"],
                round_id=round_raw_data["data"]["id"],
                home_team_id=game_raw_data["data"]["home"]["id"],
                away_team_id=game_raw_data["data"]["away"]["id"],
                date=game_raw_data["data"]["date"],
                game_status=game_raw_data["data"]["status"],
                home_team_score=home_team_score,
                away_team_score=away_team_score
            )
        
        except ValidationError as e:
            raise ValueError(f"Error al procesar el partido {season}/R{round}/{game_name}: {e}")
        
        return game

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
    
    def _get_player_events(self, events_raw_data: List[Dict], player_performance_id: UUID) -> List[Event] | str:
        """
        Procesa los eventos de un jugador en un partido específico.
        
        Args:
            events_raw_data (list): Eventos del jugador.
            player_performance_id (UUID): ID de la actuación del jugador.
        
        Returns:
            List[Event]: Eventos del jugador en el partido.
        """
        events: List[Event] = []
        for raw_event in events_raw_data:
            try:
                event_id: UUID = uuid4()
                event: Event = Event(
                    event_id=event_id,
                    event_type=raw_event["type"],
                    player_performance_id=player_performance_id,
                    event_minute=raw_event["metadata"] if "metadata" in raw_event else -1,
                )
            except (ValidationError, ValueError) as e:
                return str(object=e)
            except KeyError as e:
                return str(object=raw_event)
            events.append(event)
        return events
    
    def _get_player_game(self, player_raw_data: Dict, team_id: int, game_id: int) -> Tuple[PlayerPerformance, List[Event], PerformanceScore]:
        """
        Procesa el rendimiento de un jugador en un partido específico.
        
        Args:
            player_raw_data (dict): Datos del jugador.
            team_id (int): ID del equipo.
            game_id (int): ID del partido.
        
        Returns:
            PlayerPerformance: Rendimiento del jugador en el partido.
            List[Event]: Eventos del jugador en el partido.
            PerformanceScore: Puntuación del jugador en el partido.
        """
        player_performance_id: UUID = uuid4()        
        player_events: List[Event] | str = self._get_player_events(
            events_raw_data=player_raw_data["events"],
            player_performance_id=player_performance_id
        ) if "events" in player_raw_data else []

        if isinstance(player_events, str):
            raise ValueError(f"Error al procesar los eventos del jugador {player_raw_data['player']['name']} en {game_id}: {player_events}")

        player_performance: PlayerPerformance = PlayerPerformance(
            player_performance_id=player_performance_id,
            player_id=player_raw_data["player"]["id"],
            game_id=game_id,
            team_id=team_id
        )

        score_id: UUID = uuid4()
        performance_score: PerformanceScore = PerformanceScore(
            score_id=score_id,
            player_performance_id=player_performance_id,
            scoring_system_id=self.score,
            points=player_raw_data.get("points", None)
        )

        return player_performance, player_events, performance_score
    
    def _get_game_performances(self, game_name: str, round: int, season: int, score: Optional[int] = None) -> Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]]:
        """
        Procesa las actuaciones de los jugadores en un partido específico.
        
        Args:
            game_name (str): Nombre del archivo JSON del partido.
            round (int): Número de la jornada.
            season (int): Año de la temporada.
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        
        Returns:
            Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]]: Actuaciones de los jugadores, eventos y puntuaciones del partido.
        """
        game_raw_data: Dict = self._load_game(game_name=game_name, round=round, season=season, score=score)
        
        player_performances: List[PlayerPerformance] = []
        events: List[Event] = []
        performance_scores: List[PerformanceScore] = []
        
        for team in ["home", "away"]:
            for player_raw_data in game_raw_data["data"][team]["reports"]:
                player_game: Tuple[PlayerPerformance, List[Event], PerformanceScore] = self._get_player_game(
                    player_raw_data=player_raw_data,
                    team_id=game_raw_data["data"][team]["id"],
                    game_id=game_raw_data["data"]["id"]
                )
                
                player_performance: PlayerPerformance = player_game[0]
                player_events: List[Event] = player_game[1]
                performance_score: PerformanceScore = player_game[2]
                
                player_performances.append(player_performance)
                events.extend(player_events)
                performance_scores.append(performance_score)

        return player_performances, events, performance_scores
    
    def _get_round_performances(self, round: int, season: int, score: Optional[int] = None) -> Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]]:
        """
        Procesa las actuaciones de los jugadores en una jornada específica.
        
        Args:
            round (int): ID de la jornada.
            season (int): ID de la temporada.
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        
        Returns:
            Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]]: Actuaciones de los jugadores, eventos y puntuaciones de la jornada.
        """
        if score is None:
            scoring_folder: str = self.scoring_folder
        else:
            scoring_folder: str = self._get_scoring_folder(score=score)

        round_performances: List[PlayerPerformance] = []
        round_events: List[Event] = []
        round_scores: List[PerformanceScore] = []
        
        for game_name in os.listdir(path=os.path.join("data/JSONs/Games", scoring_folder, str(object=season), f"R{round}")):
            if game_name.endswith(".json"):
                game_name: str = game_name[:-5]
                game: Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]] = self._get_game_performances(
                    game_name=game_name,
                    round=round,
                    season=season,
                    score=score
                )

                game_performances: List[PlayerPerformance] = game[0]
                game_events: List[Event] = game[1]
                game_scores: List[PerformanceScore] = game[2]
                
                round_performances.extend(game_performances)
                round_events.extend(game_events)
                round_scores.extend(game_scores)

        return round_performances, round_events, round_scores

    def _get_season_performances(self, season: int, score: Optional[int] = None) -> Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]]:
        """
        Procesa las actuaciones de los jugadores en una temporada específica.
        
        Args:
            season (int): ID de la temporada.
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        
        Returns:
            Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]]: Actuaciones de los jugadores, eventos y puntuaciones de la temporada.
        """
        if score is None:
            scoring_folder: str = self.scoring_folder
        else:
            scoring_folder: str = self._get_scoring_folder(score=score)

        season_performances: List[PlayerPerformance] = []
        season_events: List[Event] = []
        season_scores: List[PerformanceScore] = []

        for round in os.listdir(path=os.path.join("data/JSONs/Games", scoring_folder, str(object=season))):
            if os.path.isdir(s=os.path.join("data/JSONs/Games", scoring_folder, str(object=season), round)):
                round_id: int = int(round[1:])
                round_performances: Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]] = self._get_round_performances(
                    round=round_id,
                    season=season,
                    score=score
                )

                performances: List[PlayerPerformance] = round_performances[0]
                events: List[Event] = round_performances[1]
                scores: List[PerformanceScore] = round_performances[2]

                season_performances.extend(performances)
                season_events.extend(events)
                season_scores.extend(scores)

        return season_performances, season_events, season_scores

    def get_performances(self, score: Optional[int] = None) -> Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]]:
        """
        Devuelve las actuaciones de los jugadores y eventos de la temporada actual.
        
        Args:
            score (int, optional): Sistema de puntuación a utilizar. Por defecto es el sistema de puntuación actual.
        
        Returns:
            Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]]: Actuaciones de los jugadores, eventos y puntuaciones de la temporada.
        """
        if score is None:
            scoring_folder: str = self.scoring_folder
        else:
            scoring_folder: str = self._get_scoring_folder(score=score)

        performances: List[PlayerPerformance] = []
        events: List[Event] = []
        scores: List[PerformanceScore] = []

        for season in os.listdir(path=os.path.join("data/JSONs/Games", scoring_folder)):
            if os.path.isdir(s=os.path.join("data/JSONs/Games", scoring_folder, season)):
                season_id: int = int(season)
                season_performances: Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]] = self._get_season_performances(
                    season=season_id,
                    score=score
                )

                performances.extend(season_performances[0])
                events.extend(season_performances[1])
                scores.extend(season_performances[2])
        
        return performances, events, scores

    def _get_player(self, player_raw_data: Dict) -> Player:
        """
        Procesa los datos de un jugador y devuelve su información.

        Args:
            player_raw_data (dict): Datos del jugador.

        Returns:
            Player: Información del jugador.
        """
        return Player(
            player_id=player_raw_data["id"],
            player_name=player_raw_data["name"],
            player_position=player_raw_data["position"]
        )
    
    def _get_game_players(self, game_name: str, round: int, season: int, seen_player_ids: set) -> List[Player]:
        """
        Procesa los jugadores de un partido específico.
        
        Args:
            game_name (str): Nombre del archivo JSON del partido.
            round (int): Número de la jornada.
            season (int): Año de la temporada.
            seen_player_ids (set): Conjunto de IDs de jugadores ya procesados.
        
        Returns:
            List[Player]: Lista de jugadores en el partido.
        """
        game_raw_data: Dict = self._load_game(game_name=game_name, round=round, season=season)
        
        players: List[Player] = []
        for team in ["home", "away"]:
            for player_raw_data in game_raw_data["data"][team]["reports"]:
                player_id: int = player_raw_data["player"]["id"]
                if player_id not in seen_player_ids:
                    players.append(self._get_player(player_raw_data=player_raw_data["player"]))
                    seen_player_ids.add(player_id)
        
        return players
    
    def _get_round_players(self, round: int, season: int, seen_player_ids: set) -> List[Player]:
        """
        Procesa los jugadores de una jornada específica.
        
        Args:
            round (int): ID de la jornada.
            season (int): ID de la temporada.
            seen_player_ids (set): Conjunto de IDs de jugadores ya procesados.
        
        Returns:
            List[Player]: Lista de jugadores en la jornada.
        """
        players: List[Player] = []
        for game_name in os.listdir(path=os.path.join("data/JSONs/Games", self.scoring_folder, str(object=season), f"R{round}")):
            if game_name.endswith(".json"):
                game_name: str = game_name[:-5]
                players.extend(self._get_game_players(game_name=game_name, round=round, season=season, seen_player_ids=seen_player_ids))
        
        return players
    
    def _get_season_players(self, season: int, seen_player_ids: set) -> List[Player]:
        """
        Procesa los jugadores de una temporada específica.
        
        Args:
            season (int): ID de la temporada.
            seen_player_ids (set): Conjunto de IDs de jugadores ya procesados.
        
        Returns:
            List[Player]: Lista de jugadores en la temporada.
        """
        players: List[Player] = []
        for round in os.listdir(path=os.path.join("data/JSONs/Games", self.scoring_folder, str(object=season))):
            if os.path.isdir(s=os.path.join("data/JSONs/Games", self.scoring_folder, str(object=season), round)):
                round_id: int = int(round[1:])
                players.extend(self._get_round_players(round=round_id, season=season, seen_player_ids=seen_player_ids))
        
        return players
    
    def get_players(self) -> List[Player]:
        """
        Devuelve una lista con todos los jugadores disponibles.

        Returns:
            List[Player]: Lista de jugadores.
        """
        players: List[Player] = []
        seen_player_ids: set = set()
        
        for season in os.listdir(path=os.path.join("data/JSONs/Games", self.scoring_folder)):
            if os.path.isdir(s=os.path.join("data/JSONs/Games", self.scoring_folder, season)):
                season_id: int = int(season)
                players.extend(self._get_season_players(season=season_id, seen_player_ids=seen_player_ids))
        
        return players
    
    def _get_team(self, team_raw_data: Dict) -> Team:
        """
        Procesa los datos de un equipo y devuelve su información.

        Args:
            team_raw_data (dict): Datos del equipo.

        Returns:
            Team: Información del equipo.
        """
        return Team(
            team_id=team_raw_data["id"],
            team_name=team_raw_data["name"]
        )
    
    def _get_game_teams(self, game_name: str, round: int, season: int, seen_teams_ids: set) -> List[Team]:
        """
        Procesa los equipos de un partido específico.
        
        Args:
            game_name (str): Nombre del archivo JSON del partido.
            round (int): Número de la jornada.
            season (int): Año de la temporada.
            seen_teams_ids (set): Conjunto de IDs de equipos ya procesados.
        
        Returns:
            List[Team]: Lista de equipos en el partido.
        """
        game_raw_data: Dict = self._load_game(game_name=game_name, round=round, season=season)
        
        teams: List[Team] = []
        for team in ["home", "away"]:
            team_id: int = game_raw_data["data"][team]["id"]
            if team_id not in seen_teams_ids:
                seen_teams_ids.add(team_id)
                teams.append(self._get_team(team_raw_data=game_raw_data["data"][team]))
        
        return teams
    
    def _get_round_teams(self, round: int, season: int, seen_teams_ids: set) -> List[Team]:
        """
        Procesa los equipos de una jornada específica.
        
        Args:
            round (int): ID de la jornada.
            season (int): ID de la temporada.
            seen_teams_ids (set): Conjunto de IDs de equipos ya procesados.
        
        Returns:
            List[Team]: Lista de equipos en la jornada.
        """
        teams: List[Team] = []
        for game_name in os.listdir(path=os.path.join("data/JSONs/Games", self.scoring_folder, str(object=season), f"R{round}")):
            if game_name.endswith(".json"):
                game_name: str = game_name[:-5]
                teams.extend(self._get_game_teams(game_name=game_name, round=round, season=season, seen_teams_ids=seen_teams_ids))
        
        return teams
    
    def _get_season_teams(self, season: int, seen_teams_ids: set) -> List[Team]:
        """
        Procesa los equipos de una temporada específica.
        
        Args:
            season (int): ID de la temporada.
            seen_teams_ids (set): Conjunto de IDs de equipos ya procesados.
        
        Returns:
            List[Team]: Lista de equipos en la temporada.
        """
        teams: List[Team] = []
        for round in os.listdir(path=os.path.join("data/JSONs/Games", self.scoring_folder, str(object=season))):
            if os.path.isdir(s=os.path.join("data/JSONs/Games", self.scoring_folder, str(object=season), round)):
                round_id: int = int(round[1:])
                teams.extend(self._get_round_teams(round=round_id, season=season, seen_teams_ids=seen_teams_ids))
        
        return teams
    
    def get_teams(self) -> List[Team]:
        """
        Devuelve una lista con todos los equipos disponibles.

        Returns:
            List[Team]: Lista de equipos.
        """
        teams: List[Team] = []
        seen_teams_ids: set = set()
        
        for season in os.listdir(path=os.path.join("data/JSONs/Games", self.scoring_folder)):
            if os.path.isdir(s=os.path.join("data/JSONs/Games", self.scoring_folder, season)):
                season_id: int = int(season)
                teams.extend(self._get_season_teams(season=season_id, seen_teams_ids=seen_teams_ids))
        
        return teams

if __name__ == "__main__":
    processor: BiwengerJSONProcessor = BiwengerJSONProcessor()
    
    for season in processor.get_seasons():
        print(season) 
        break

    for round in processor.get_rounds():
        print(round)
        break

    for game in processor.get_games():
        print(game)
        break
    
    performances: Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]] = processor.get_performances()
    for performance, event, score in zip(performances[0], performances[1], performances[2]):
        print(performance)
        print(event)
        print(score)
        break

    for player in processor.get_players():
        print(player)
        break

    for team in processor.get_teams():
        print(team)
        break