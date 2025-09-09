from pydantic import BaseModel, Field
from typing import Optional

class ProblemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    concept: str = Field(..., min_length=1, max_length=50)
    stars: int = Field(..., ge=1, le=5)
    series_id: Optional[int] = None
    series_index: Optional[int] = None
    is_daily_candidate: bool = True

class ProblemCreate(ProblemBase):
    pass

class ProblemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    concept: Optional[str] = Field(None, min_length=1, max_length=50)
    stars: Optional[int] = Field(None, ge=1, le=5)
    series_id: Optional[int] = None
    series_index: Optional[int] = None
    is_daily_candidate: Optional[bool] = None

class ProblemResponse(ProblemBase):
    id: int

    class Config:
        from_attributes = True