from typing import Dict, List

from postgrest.base_request_builder import APIResponse

from src.db_processor.connection import DatabaseConnection
from src.json_processor.processor import BiwengerJSONProcessor
from src.json_processor.definitions import Season

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BiwengerDBProcessor:
    db: DatabaseConnection
    json_processor: BiwengerJSONProcessor

    def __init__(self) -> None:
        self.db = DatabaseConnection()
        self.json_processor = BiwengerJSONProcessor()

    def _upload_season(self, season: Season) -> None:
        """
        Uploads the season data to the database.
        """
        season_data: Dict = season.to_dict()
        logging.info(msg=f"Uploading season data: {season_data['season_name']}")
        response: APIResponse = self.db.supabase.table(table_name="seasons").insert(json=season_data).execute()
        logging.info(msg=f"Supabase Response: {response.data}")
    
    def upload_seasons(self) -> None:
        """
        Uploads all seasons to the database.
        """
        seasons: List[Season] = self.json_processor.get_seasons()
        for season in seasons:
            self._upload_season(season=season)
        logging.info(msg=f"Uploaded {len(seasons)} seasons to the database.")
    

if __name__ == "__main__":
    processor: BiwengerDBProcessor = BiwengerDBProcessor()
    processor.upload_seasons()