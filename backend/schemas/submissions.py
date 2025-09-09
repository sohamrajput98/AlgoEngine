from pydantic import BaseModel

class SubmissionCreate(BaseModel):
    code: str
    language: str

class SubmissionResponse(BaseModel):
    id: int
    problem_id: int
    user_id: int
    code: str
    language: str
    status: str

    class Config:
        orm_mode = True
