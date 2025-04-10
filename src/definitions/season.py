from typing import Dict
from pydantic import BaseModel

from src.definitions.status import Status

class Season(BaseModel):
    season_id: int # ID de la temporada
    season_name: str # Nombre de la temporada
    season_status: str # Estado de la temporada
    _status: Status = Status.DESCONOCIDO # Estado de la temporada (automáticamente generado)

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._status = Status.from_value(value=self.season_status)

    @classmethod
    def from_dict(cls, data: Dict) -> "Season":
        """
        Crea un objeto Season a partir de un diccionario.
        """
        return cls(**data)

    def to_dict(self) -> Dict:
        """
        Convierte el objeto Season a un diccionario.
        """
        return {
            "season_id": self.season_id,
            "season_name": self.season_name,
            "season_status": self._status.value,
            #"_status": self._status.value
        }

    def __str__(self) -> str:
        """
        Devuelve una representación en string de la temporada.
        """
        return f"{'-' * 30}\nTemporada\nID: {self.season_id}\nNombre: {self.season_name}\nEstado: {self._status.get_value()}\n{'-' * 30}"