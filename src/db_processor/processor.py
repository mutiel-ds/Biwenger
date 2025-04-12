from uuid import uuid4
from typing import Dict, List, Tuple, Set

from postgrest.exceptions import APIError
from postgrest.base_request_builder import APIResponse

from src.config import PK_COLUMNS
from src.db_processor.connection import DatabaseConnection
from src.json_processor.processor import BiwengerJSONProcessor
from src.definitions import (
    Season, 
    Round, 
    Player, 
    Team, 
    Game,
    PlayerPerformance,
    Event,
    PerformanceScore
)

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BiwengerDBProcessor:
    db: DatabaseConnection
    json_processor: BiwengerJSONProcessor

    def __init__(self) -> None:
        self.db = DatabaseConnection()
        self.json_processor = BiwengerJSONProcessor()

    def get_player_performances(self) -> Set:
        """
        Returns all player performances from the database.
        
        This method retrieves all player performances from the database using pagination
        to handle tables with more than 1000 rows (Supabase's default limit).
        
        Returns:
            Set: A set of tuples containing player_id and game_id for all player performances.
        """
        player_performances: Set = set()
        offset: int = 0
        limit: int = 1000
        has_more: bool = True
        
        while has_more:
            response: APIResponse = self.db.supabase.table(table_name="player_performances").select("player_id,game_id").range(offset, offset + limit - 1).execute()
            
            if not response.data or len(response.data) == 0:
                has_more = False
            else:
                for row in response.data:
                    player_performances.add((row["player_id"], row["game_id"]))
                
                offset += limit
                
                if len(response.data) < limit:
                    has_more = False
        
        return player_performances

    def _post_season(self, season: Season) -> None:
        """
        Uploads the season data to the database.
        """
        season_data: Dict = season.to_dict()
        logging.info(msg=f"Uploading season data: {season_data['season_name']}")
        try:
            response: APIResponse = self.db.supabase.table(table_name="seasons").insert(json=season_data).execute()
            logging.info(msg=f"Supabase Response: {response.data}")
        except APIError as e:
            logging.error(msg=f"Error uploading season data: (code:{e.code}) {e.message} [details:'{e.details}']")
    
    def post_seasons(self) -> None:
        """
        Uploads all seasons to the database.
        """
        seasons: List[Season] = self.json_processor.get_seasons()
        seasons_data: List[Dict] = [season.to_dict() for season in seasons]
        total_seasons: int = len(seasons_data)
        try:
            self.db.supabase.table(table_name="seasons").insert(json=seasons_data).execute()
            logging.info(msg=f"Uploaded {total_seasons} seasons to the database in batch operations.")
        except APIError as e:
            logging.error(msg=f"Error uploading batch of seasons: (code:{e.code}) {e.message} [details:'{e.details}']")
    
    def _post_round(self, round: Round) -> None:
        """
        Uploads the round data to the database.
        """
        round_data: Dict = round.to_dict()
        logging.info(msg=f"Uploading round data: {round_data['round_name']}")
        try:
            response: APIResponse = self.db.supabase.table(table_name="rounds").insert(json=round_data).execute()
            logging.info(msg=f"Supabase Response: {response.data}")
        except APIError as e:
            logging.error(msg=f"Error uploading round data: (code:{e.code}) {e.message} [details:'{e.details}']")

    def post_rounds(self) -> None:
        """
        Uploads all rounds to the database.
        """
        rounds: List[Round] = self.json_processor.get_rounds()
        rounds_data: List[Dict] = [round.to_dict() for round in rounds]
        total_rounds: int = len(rounds_data)
        try:
            self.db.supabase.table(table_name="rounds").insert(json=rounds_data).execute()
            logging.info(msg=f"Uploaded {total_rounds} rounds to the database in batch operations.")
        except APIError as e:
            logging.error(msg=f"Error uploading batch of rounds: (code:{e.code}) {e.message} [details:'{e.details}']")

    def _post_team(self, team: Team) -> None:
        """
        Uploads the team data to the database.
        """
        team_data: Dict = team.to_dict()
        logging.info(msg=f"Uploading team data: {team_data['team_name']}")
        try:
            response: APIResponse = self.db.supabase.table(table_name="teams").insert(json=team_data).execute()
            logging.info(msg=f"Supabase Response: {response.data}")
        except APIError as e:
            logging.error(msg=f"Error uploading team data: (code:{e.code}) {e.message} [details:'{e.details}']")

    def post_teams(self) -> None:
        """
        Uploads all teams to the database.
        """
        teams: List[Team] = self.json_processor.get_teams()
        teams_data: List[Dict] = [team.to_dict() for team in teams]
        total_teams: int = len(teams_data)
        try:
            self.db.supabase.table(table_name="teams").insert(json=teams_data).execute()
            logging.info(msg=f"Uploaded {total_teams} teams to the database in batch operations.")
        except APIError as e:
            logging.error(msg=f"Error uploading batch of teams: (code:{e.code}) {e.message} [details:'{e.details}']")

    def _post_game(self, game: Game) -> None:
        """
        Uploads the game data to the database.
        """
        game_data: Dict = game.to_dict()
        logging.info(msg=f"Uploading game data: {game_data['game_id']}")
        try:
            response: APIResponse = self.db.supabase.table(table_name="games").insert(json=game_data).execute()
            logging.info(msg=f"Supabase Response: {response.data}")
        except APIError as e:
            logging.error(msg=f"Error uploading game data: (code:{e.code}) {e.message} [details:'{e.details}']")

    def post_games(self) -> None:
        """
        Uploads all games to the database.
        """
        games: List[Game] = self.json_processor.get_games()
        games_data: List[Dict] = [game.to_dict() for game in games]
        total_games: int = len(games_data)
        try:
            self.db.supabase.table(table_name="games").insert(json=games_data).execute()
            logging.info(msg=f"Uploaded {total_games} games to the database in batch operations.")
        except APIError as e:
            logging.error(msg=f"Error uploading batch of games: (code:{e.code}) {e.message} [details:'{e.details}']")

    def _post_player(self, player: Player) -> None:
        """
        Uploads the player data to the database.
        """
        player_data: Dict = player.to_dict()
        logging.info(msg=f"Uploading player data: {player_data['player_name']}")
        try:
            response: APIResponse = self.db.supabase.table(table_name="players").insert(json=player_data).execute()
            logging.info(msg=f"Supabase Response: {response.data}")
        except APIError as e:
            logging.error(msg=f"Error uploading player data: (code:{e.code}) {e.message} [details:'{e.details}']")
        
    def post_players(self) -> None:
        """
        Uploads all players to the database.
        """
        players: List[Player] = self.json_processor.get_players()
        players_data: List[Dict] = [player.to_dict() for player in players]
        total_players: int = len(players)
        try:
            self.db.supabase.table(table_name="players").insert(json=players_data).execute()
            logging.info(msg=f"Uploaded {total_players} players to the database in batch operations.")
        except APIError as e:
            logging.error(msg=f"Error uploading batch of players: (code:{e.code}) {e.message} [details:'{e.details}']")

    def _post_player_performance(self, player_performance: PlayerPerformance) -> None:
        """
        Uploads the player performance data to the database.
        """
        player_performance_data: Dict = player_performance.to_dict()
        logging.info(msg=f"Uploading player performance data: {player_performance_data['player_performance_id']}")
        try:
            response: APIResponse = self.db.supabase.table(table_name="player_performances").insert(json=player_performance_data).execute()
            logging.info(msg=f"Supabase Response: {response.data}")
        except APIError as e:
            logging.error(msg=f"Error uploading player performance data: (code:{e.code}) {e.message} [details:'{e.details}']")

    def _post_player_events(self, event: Event) -> None:
        """
        Uploads the player events data to the database.
        """
        event_data: Dict = event.to_dict()
        logging.info(msg=f"Uploading player event data: {event_data['event_id']}")
        try:
            response: APIResponse = self.db.supabase.table(table_name="events").insert(json=event_data).execute()
            logging.info(msg=f"Supabase Response: {response.data}")
        except APIError as e:
            logging.error(msg=f"Error uploading player event data: (code:{e.code}) {e.message} [details:'{e.details}']")

    def _post_player_score(self, score: PerformanceScore) -> None:
        """
        Uploads the player score data to the database.
        """
        score_data: Dict = score.to_dict()
        logging.info(msg=f"Uploading player score data: {score_data['score_id']}")
        try:
            response: APIResponse = self.db.supabase.table(table_name="performance_scores").insert(json=score_data).execute()
            logging.info(msg=f"Supabase Response: {response.data}")
        except APIError as e:
            logging.error(msg=f"Error uploading player score data: (code:{e.code}) {e.message} [details:'{e.details}']")

    def _post_player_performances(self, player_performances: List[PlayerPerformance]) -> None:
        """
        Uploads all player performances to the database in batch operations.
        
        This method checks if each player performance already exists in the database
        before attempting to upload it, to avoid duplicate entries. It then uploads
        the new performances in batches for better performance.
        """
        if not player_performances:
            logging.info(msg="No player performances to upload.")
            return
        
        performances_data: List[Dict] = [performance.to_dict() for performance in player_performances]
        total_performances: int = len(performances_data)
        try:
            self.db.supabase.table(table_name="player_performances").insert(json=performances_data).execute()
            logging.info(msg=f"Uploaded {total_performances} player performances to the database in batch operations.")
        except APIError as e:
            logging.error(msg=f"Error uploading batch of player performances: (code:{e.code}) {e.message} [details:'{e.details}']")

    def _post_players_events(self, events: List[Event]) -> None:
        """
        Uploads all player events to the database in a single batch operation.
        
        This method converts all events to dictionaries and inserts them in a single
        database request, which is much more efficient than individual inserts.
        """
        if not events:
            logging.info(msg="No events to upload.")
            return
        
        events_data: List[Dict] = [event.to_dict() for event in events]
        total_events: int = len(events_data)
        try:
            self.db.supabase.table(table_name="events").insert(json=events_data).execute()
            logging.info(msg=f"Uploaded {total_events} player events to the database in batch operations.")
        except APIError as e:
            logging.error(msg=f"Error uploading batch of events: (code:{e.code}) {e.message} [details:'{e.details}']")
    
    def _post_player_scores(self, scores: List[PerformanceScore]) -> None:
        """
        Uploads all player scores to the database in a single batch operation.
        
        This method converts all scores to dictionaries and inserts them in a single
        database request, which is much more efficient than individual inserts.
        """
        if not scores:
            logging.info(msg="No scores to upload.")
            return
        
        scores_data: List[Dict] = [score.to_dict() for score in scores]
        total_scores: int = len(scores_data)
        try:
            self.db.supabase.table(table_name="performance_scores").insert(json=scores_data).execute()
            logging.info(msg=f"Uploaded {total_scores} player scores to the database in batch operations.")
        except APIError as e:
            logging.error(msg=f"Error uploading batch of scores: (code:{e.code}) {e.message} [details:'{e.details}']")
    
    def post_performances(self, 
            post_performances: bool = True,
            post_events: bool = True,
            post_scores: bool = True,
        ) -> None:
        """
        Uploads all player performances to the database.
        """
        performances: Tuple[List[PlayerPerformance], List[Event], List[PerformanceScore]] = self.json_processor.get_performances()
        player_performances: List[PlayerPerformance] = performances[0]
        events: List[Event] = performances[1]
        scores: List[PerformanceScore] = performances[2]

        if post_performances:
            self._post_player_performances(player_performances=player_performances)

        if post_events:
            self._post_players_events(events=events)

        if post_scores:
            self._post_player_scores(scores=scores)

    def delete_table_data(self, table_name: str) -> None:
        """
        Deletes all rows from a specified table in the database.
        
        This method uses a mapping of table names to their primary key columns to
        construct the DELETE operation. Use with caution as this operation cannot be undone.
        
        Args:
            table_name (str): The name of the table to delete all rows from.
        """
        logging.info(msg=f"Deleting all rows from table: {table_name}")
        try:
            pk: Dict = PK_COLUMNS.get(table_name, {})
            if not pk:
                logging.error(msg=f"Unknown primary key column for table: {table_name}")
                return
            
            pk_column: str = pk["column"]
            pk_value: int | str = pk["value"]
            self.db.supabase.table(table_name=table_name).delete().neq(column=pk_column, value=pk_value).execute()            
            logging.info(msg=f"Successfully deleted all rows from table: {table_name}")

        except APIError as e:
            logging.error(msg=f"Error deleting rows from table {table_name}: (code:{e.code}) {e.message} [details:'{e.details}']")

    def delete_data(self) -> None:
        """
        Deletes all data from  the database.
        """
        logging.info(msg="Deleting all data from the database")
        for table_name in PK_COLUMNS.keys():
            self.delete_table_data(table_name=table_name)

def main() -> None:
    """
    Main function to run the BiwengerDBProcessor.
    """
    processor = BiwengerDBProcessor()
    processor.delete_data()
    processor.post_seasons()
    processor.post_rounds()
    processor.post_teams()
    processor.post_players()
    processor.post_games()
    processor.post_performances()

if __name__ == "__main__":
    main()