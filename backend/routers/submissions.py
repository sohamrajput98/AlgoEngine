from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import tempfile
import subprocess

from db import SessionLocal
from models.submission import Submission
from models.problem import Problem
from models.testcase import TestCase
from models.user import User
from dependencies import get_current_user
 # import your auth dependency

router = APIRouter(prefix="/submissions", tags=["submissions"])


# -------------------------
# DATABASE DEPENDENCY
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Pydantic model
# -------------------------
class SubmissionCreate(BaseModel):
    code: str
    language: str


# -------------------------
# CREATE SUBMISSION
# -------------------------
@router.post("/problems/{problem_id}/submit")
def create_submission(
    problem_id: int,
    submission: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    db_submission = Submission(
        problem_id=problem_id,
        user_id=current_user.id,
        code=submission.code,
        language=submission.language,
        status="pending"
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)

    testcases = db.query(TestCase).filter(TestCase.problem_id == problem_id).all()
    if not testcases:
        raise HTTPException(status_code=400, detail="No testcases for this problem")

    all_passed = True

    if submission.language.lower() == "python":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmpfile:
            tmpfile.write(submission.code.encode())
            tmpfile.flush()

            for tc in testcases:
                try:
                    result = subprocess.run(
                        ["python3", tmpfile.name],
                        input=tc.input_data.encode(),
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    output = result.stdout.strip()
                    if output != tc.expected_output.strip():
                        all_passed = False
                        break
                except subprocess.TimeoutExpired:
                    all_passed = False
                    break
    else:
        db_submission.status = "unsupported_language"
        db.commit()
        return {"id": db_submission.id, "status": db_submission.status}

    db_submission.status = "passed" if all_passed else "failed"
    db.commit()
    db.refresh(db_submission)
    return {"id": db_submission.id, "status": db_submission.status}


# -------------------------
# GET SUBMISSION
# -------------------------
@router.get("/{submission_id}")
def get_submission(submission_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if submission.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to view this submission")
    return {
        "problem_id": submission.problem_id,
        "user_id": submission.user_id,
        "code": submission.code,
        "language": submission.language,
        "status": submission.status
    }
