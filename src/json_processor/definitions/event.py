from enum import Enum
from typing import Dict
from uuid import uuid4, UUID
from pydantic import BaseModel

class EventType(Enum):
    DESCONOCIDO = 0
    GOL = 1
    GOL_PENALTI = 2
    ASISTENCIA = 3
    SUSTITUCION = 4
    ENTRADA_BANQUILLO = 5
    TARJETA_AMARILLA = 6
    TAREJETA_ROJA = 7
    DOBLE_TARJETA_AMARILLA = 8
    AUTOGOL = 9
    DISPARO_AL_PALO = 10
    PENALTI_FALLADO = 11
    PENALTI_PARADO = 12
    GOL_ANULADO = 13
    LESION = 14
    PENALTI = 16

    @classmethod
    def from_value(cls, value: int) -> "EventType":
        """
        Devuelve un objeto EventType a partir de su valor.
        """
        for event_type in cls:
            if event_type.value == value:
                return event_type
        raise ValueError(f"Valor '{value}' de evento no soportado.")
    
    def get_value(self) -> int:
        """
        Devuelve el valor de un objeto EventType.
        """
        return self.value

    def get_description(self) -> str:
        """
        Devuelve la descripción de un objeto EventType.
        """ 
        descriptions: Dict[EventType, str] = {
            EventType.DESCONOCIDO: "Evento desconocido",
            EventType.GOL: "Gol",
            EventType.GOL_PENALTI: "Gol de penalti",
            EventType.ASISTENCIA: "Asistencia",
            EventType.SUSTITUCION: "Sustitución",
            EventType.ENTRADA_BANQUILLO: "Entrada desde el banquillo",
            EventType.TARJETA_AMARILLA: "Tarjeta amarilla",
            EventType.TAREJETA_ROJA: "Tarjeta roja",
            EventType.DOBLE_TARJETA_AMARILLA: "Doble tarjeta amarilla",
            EventType.AUTOGOL: "Autogol",
            EventType.DISPARO_AL_PALO: "Disparo al palo",
            EventType.PENALTI_FALLADO: "Penalti fallado",
            EventType.PENALTI_PARADO: "Penalti parado",
            EventType.GOL_ANULADO: "Gol anulado",
            EventType.LESION: "Lesión",
            EventType.PENALTI: "Penalti"
        }

        return descriptions.get(self, "Evento desconocido")

class Event(BaseModel):
    event_id: UUID = uuid4() # ID único del evento (automáticamente generado)
    player_performance_id: UUID # ID de la actuación del jugador
    event_type: int # ID del tipo de evento
    event_minute: int # Minuto del evento
    _event_description: str = "" # Descripción del evento (automáticamente generado)
    _event_type: EventType = EventType.DESCONOCIDO # Tipo de evento (automáticamente generado)

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._event_type = EventType.from_value(value=self.event_type)
        self._event_description = self._event_type.get_description()

    def __str__(self) -> str:
        """
        Devuelve una representación en string del evento.
        """
        return f"{'-' * 30}\nEvento\nID del evento: {self.event_id}\nID de actuación del jugador: {self.player_performance_id}\nTipo de evento: {self._event_description}\nMinuto: {self.event_minute}'\n{'-' * 30}"