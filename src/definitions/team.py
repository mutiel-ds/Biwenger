from pydantic import BaseModel

class Team(BaseModel):
    team_id: int # ID del equipo
    team_name: str # Nombre del equipo

    def __str__(self) -> str:
        """
        Devuelve una representación en string del equipo.
        """
        return f"{'-' * 30}\nEquipo\nID: {self.team_id}\nNombre: {self.team_name}\n{'-' * 30}"