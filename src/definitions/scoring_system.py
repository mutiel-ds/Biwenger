from enum import Enum
from typing import Dict
from uuid import UUID, uuid4
from pydantic import BaseModel

class ScoringSystemType(Enum):
    DESCONOCIDO = 0
    PICAS = 1
    SOFASCORE = 2
    MEDIA = 5

    @classmethod
    def from_value(cls, value: int) -> "ScoringSystemType":
        """
        Devuelve un objeto ScoringSystemType a partir de su valor.
        """
        for scoring_system_type in cls:
            if scoring_system_type.value == value:
                return scoring_system_type
        raise ValueError("Valor de sistema de puntuación no soportado.")
    
    def get_value(self) -> int:
        """
        Devuelve el valor de un objeto ScoringSystemType.
        """
        return self.value
    
    def get_scoring_system(self) -> str:
        """
        Devuelve la descripción de un objeto ScoringSystemType.
        """
        descriptions: Dict[ScoringSystemType, str] = {
            ScoringSystemType.DESCONOCIDO: "Sistema de puntuación desconocido",
            ScoringSystemType.PICAS: "Picas",
            ScoringSystemType.SOFASCORE: "SofaScore",
            ScoringSystemType.MEDIA: "Media"
        }

        return descriptions.get(self, "Sistema de puntuación desconocido")

class ScoringSystem(BaseModel):
    scoring_system_id: int # ID del sistema de puntuación
    scoring_system_name: str # Nombre del sistema de puntuación
    scoring_system_type: ScoringSystemType  = ScoringSystemType.DESCONOCIDO # Tipo de sistema de puntuación

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.scoring_system_type = ScoringSystemType.from_value(value=self.scoring_system_id)

class PerformanceScore(BaseModel):
    score_id: UUID = uuid4() # ID de la puntuacion
    player_performance_id: UUID # ID de la actuación del jugador
    scoring_system_id: int # ID del sistema de puntuación
    points: int | None # Puntos obtenidos por el jugador

    def __str__(self) -> str:
        """
        Devuelve una representación en string de la puntuación.
        """
        return f"{'-' * 30}\nPuntuación\nID de la puntuación: {self.score_id}\nID de la actuación del jugador: {self.player_performance_id}\nID del sistema de puntuación: {self.scoring_system_id}\nPuntos: {self.points}\n{'-' * 30}"

    @classmethod
    def from_dict(cls, data: Dict) -> "PerformanceScore":
        """
        Crea un objeto PerformanceScore a partir de un diccionario.
        """
        return cls(**data)
    
    def to_dict(self) -> Dict:
        """
        Convierte el objeto PerformanceScore a un diccionario.
        """
        return {
            "score_id": str(object=self.score_id),
            "player_performance_id": str(object=self.player_performance_id),
            "scoring_system_id": self.scoring_system_id,
            "points": self.points
        }