from pydantic import BaseModel

class AlertParameterDTO(BaseModel):
    maxFeedingTimeMinutes: int
    maxIntervalWithoutFeedingHours: int
    rfidReadTolerance: int
    minAmountWithoutAlertGrams: int
