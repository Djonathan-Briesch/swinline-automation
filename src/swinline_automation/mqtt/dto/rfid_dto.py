from pydantic import BaseModel, Field, field_validator

class RFIDDTO(BaseModel):
    rfid: str = Field(..., description="RFID do animal")

    @field_validator("rfid")
    def validate_rfid_length(model_cls, rfid_value):
        if len(rfid_value) <= 5:
            raise ValueError("O RFID deve ter mais de 5 caracteres")
        return rfid_value
