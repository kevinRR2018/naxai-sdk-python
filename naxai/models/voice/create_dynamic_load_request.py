from pydantic import BaseModel, Field

class CreateDynamicLoadRequest(BaseModel):
    name: str = Field(alias="name", max_length=20, min_length=3)
    max_rate: int = Field(alias="maxRate", ge=1, le=15)