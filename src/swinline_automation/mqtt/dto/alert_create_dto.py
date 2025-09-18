from pydantic import BaseModel, Field, field_validator, root_validator
from datetime import datetime
from enum import Enum
from typing import Optional


class AlertType(str, Enum):
    NoFeeding = "NoFeeding"
    FeederTimeExceeded = "FeederTimeExceeded"
    ReadFailure = "ReadFailure"
    LowConsumption = "LowConsumption"


class AlertStatus(str, Enum):
    Pending = "Pending"
    Resolved = "Resolved"


class AlertCreateDTO(BaseModel):
    confinementId: Optional[int] = Field(
        None, description="ID do confinamento associado, se houver"
    )
    feedingRecordId: Optional[int] = Field(
        None, description="ID do registro de alimentação associado, se houver"
    )
    type: AlertType = Field(..., description="Tipo do alerta")
    description: str = Field(..., description="Descrição detalhada do alerta")
    status: AlertStatus = Field(..., description="Status inicial do alerta")
    createdAt: Optional[datetime] = Field(
        default_factory=datetime, description="Data e hora de criação do alerta"
    )

    @field_validator("description")
    def validate_description_not_empty(cls, description_value: str) -> str:
        if not description_value.strip():
            raise ValueError("description não pode ser vazia")
        return description_value
