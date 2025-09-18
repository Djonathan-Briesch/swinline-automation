from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class FeedingConsumptionLogDTO(BaseModel):
    entryDateTime: datetime = Field(..., description="Data e hora que o animal entrou")
    exitDateTime: datetime = Field(..., description="Data e hora que o animal saiu")
    amountConsumed: int = Field(
        ..., gt=0, description="Quantidade em gramas de ração consumida (maior que 0)"
    )
    confinementId: int = Field(..., gt=0, description="ID do confinamento")

    @field_validator("exitDateTime")
    def validate_exit_after_entry(
        model_cls, exit_datetime: datetime, values: dict
    ) -> datetime:
        entry_datetime: datetime = values["entryDateTime"]
        if exit_datetime <= entry_datetime:
            raise ValueError("exitDateTime deve ser posterior a entryDateTime")
        return exit_datetime

    @field_validator("entryDateTime")
    def validate_entry_not_future(model_cls, entry_datetime: datetime) -> datetime:
        if entry_datetime > datetime.now():
            raise ValueError("entryDateTime não pode ser no futuro")
        return entry_datetime
