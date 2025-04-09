from pydantic import BaseModel

class Team(BaseModel):
    team_id: int # ID del equipo
    team_name: str # Nombre del equipo

    @classmethod
    def from_dict(cls, data: dict) -> "Team":
        """
        Crea un objeto Team a partir de un diccionario.
        """
        return cls(**data)

    def to_dict(self) -> dict:
        """
        Convierte el objeto Team a un diccionario.
        """
        return {
            "team_id": self.team_id,
            "team_name": self.team_name
        }

    def __str__(self) -> str:
        """
        Devuelve una representación en string del equipo.
        """
        return f"{'-' * 30}\nEquipo\nID: {self.team_id}\nNombre: {self.team_name}\n{'-' * 30}"