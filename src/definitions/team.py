from pydantic import BaseModel

class Team(BaseModel):
    team_id: int # ID del equipo
    team_name: str # Nombre del equipo