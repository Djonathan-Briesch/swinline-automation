from pydantic import BaseModel, Field

class DailyFeedingDTO(BaseModel):
    confinement_id: int = Field(..., description="ID do confinamento do animal")
    feed_amount_grams: int = Field(..., description="Quantidade de alimento permitida hoje (gramas)")
