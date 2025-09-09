import os
import jwt
import tempfile
import subprocess
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from dotenv import load_dotenv
from dependencies import get_current_user, get_db

from dependencies import get_current_user  # ADD THIS LINE
from fastapi.middleware.cors import CORSMiddleware  # ADD THIS LINE

from db import SessionLocal
from models.user import User
from models.problem import Problem
from models.testcase import TestCase
from routers import submissions  # ✅ router import

# -------------------------
# CONFIG
# -------------------------
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "secret123")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
app.include_router(submissions.router)  # ✅ add router

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# USER REGISTRATION
# -------------------------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}


# -------------------------
# LOGIN
# -------------------------
class UserLogin(BaseModel):
    username_or_email: str
    password: str


@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.username == user.username_or_email) | (User.email == user.username_or_email)
    ).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {"sub": db_user.id, "exp": datetime.utcnow() + timedelta(hours=12)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


# -------------------------
# PROFILE MANAGEMENT
# -------------------------
class ProfileUpdate(BaseModel):
    bio: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None
    portfolio_url: str | None = None
    is_private: bool | None = None




@app.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "bio": current_user.bio,
        "linkedin_url": current_user.linkedin_url,
        "github_url": current_user.github_url,
        "portfolio_url": current_user.portfolio_url,
        "is_private": current_user.is_private,
    }


@app.put("/profile")
def update_profile(
    update: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    for field, value in update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return {"message": "Profile updated successfully"}


# -------------------------
# PROBLEM MANAGEMENT
# -------------------------
class ProblemCreate(BaseModel):
    title: str
    description: str
    concept: str
    stars: int
    series_id: int | None = None
    series_index: int | None = None
    is_daily_candidate: bool = True


@app.post("/problems")
def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    db_problem = Problem(**problem.dict())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem


@app.get("/problems")
def get_all_problems(db: Session = Depends(get_db)):
    return db.query(Problem).all()


@app.get("/problems/{problem_id}")
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


# -------------------------
# TEST CASE MANAGEMENT
# -------------------------
class TestCaseCreate(BaseModel):
    input_data: str
    expected_output: str
    is_sample: bool = False


@app.post("/problems/{problem_id}/testcases")
def create_testcase(problem_id: int, testcase: TestCaseCreate, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    db_testcase = TestCase(problem_id=problem_id, **testcase.dict())
    db.add(db_testcase)
    db.commit()
    db.refresh(db_testcase)
    return db_testcase


@app.get("/problems/{problem_id}/testcases")
def get_testcases(problem_id: int, db: Session = Depends(get_db)):
    return db.query(TestCase).filter(TestCase.problem_id == problem_id).all()


@app.get("/testcases/{testcase_id}")
def get_testcase(testcase_id: int, db: Session = Depends(get_db)):
    testcase = db.query(TestCase).filter(TestCase.id == testcase_id).first()
    if not testcase:
        raise HTTPException(status_code=404, detail="TestCase not found")
    return testcase
