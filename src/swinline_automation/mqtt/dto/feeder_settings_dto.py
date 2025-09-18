import json
from pydantic import BaseModel, Field

class FeederSettingsDTO(BaseModel):
    motor_feed_on_time_seconds: int = Field(..., description="Tempo do motor ligado para liberar ração (segundos)")
    portion_amount_grams: int = Field(..., description="Quantidade de ração liberada (gramas), em relação ao tempo do motor ligado")
    portion_interval_seconds: int = Field(..., description="Intervalo entre liberação das porções (segundos)")
    entry_door_delay_seconds: int = Field(..., description="Tempo de espera após uma matriz sair, antes de abrir a porta de entrada para a próxima (segundos)")
