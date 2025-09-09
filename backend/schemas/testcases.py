from pydantic import BaseModel, Field
from typing import Optional

class TestCaseBase(BaseModel):
    input_data: str = Field(..., max_length=1000)
    expected_output: str = Field(..., max_length=1000)
    is_sample: bool = False

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseUpdate(BaseModel):
    input_data: Optional[str] = Field(None, max_length=1000)
    expected_output: Optional[str] = Field(None, max_length=1000)
    is_sample: Optional[bool] = None

class TestCaseResponse(TestCaseBase):
    id: int
    problem_id: int

    class Config:
        from_attributes = True

class TestCasePublicResponse(BaseModel):
    """Public testcase response (hides expected output for non-sample cases)"""
    id: int
    problem_id: int
    input_data: str
    is_sample: bool
    expected_output: Optional[str] = None  # Only shown for sample cases

    class Config:
        from_attributes = True