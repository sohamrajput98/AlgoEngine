from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from dependencies import get_db, get_current_admin_user
from models.problem import Problem
from schemas.problems import ProblemCreate, ProblemResponse, ProblemUpdate

router = APIRouter(prefix="/problems", tags=["problems"])

@router.post("/", response_model=ProblemResponse)
def create_problem(
    problem: ProblemCreate, 
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    """Create a new problem (admin only)"""
    db_problem = Problem(**problem.dict())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@router.get("/", response_model=list[ProblemResponse])
def get_all_problems(
    concept: Optional[str] = Query(None, description="Filter by concept"),
    stars: Optional[int] = Query(None, ge=1, le=5, description="Filter by star rating"),
    series_id: Optional[int] = Query(None, description="Filter by series ID"),
    skip: int = Query(0, ge=0, description="Skip items for pagination"),
    limit: int = Query(100, ge=1, le=100, description="Limit items for pagination"),
    db: Session = Depends(get_db)
):
    """Get all problems with optional filtering and pagination"""
    query = db.query(Problem)
    
    if concept:
        query = query.filter(Problem.concept.ilike(f"%{concept}%"))
    if stars:
        query = query.filter(Problem.stars == stars)
    if series_id:
        query = query.filter(Problem.series_id == series_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{problem_id}", response_model=ProblemResponse)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    """Get a single problem by ID"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@router.put("/{problem_id}", response_model=ProblemResponse)
def update_problem(
    problem_id: int,
    problem_update: ProblemUpdate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    """Update a problem (admin only)"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    for field, value in problem_update.dict(exclude_unset=True).items():
        setattr(problem, field, value)
    
    db.commit()
    db.refresh(problem)
    return problem

@router.delete("/{problem_id}")
def delete_problem(
    problem_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    """Delete a problem (admin only)"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    db.delete(problem)
    db.commit()
    return {"message": "Problem deleted successfully"}

@router.get("/daily-challenge/today")
def get_daily_challenge(db: Session = Depends(get_db)):
    """Get today's daily challenge problem"""
    # Simple implementation - get a random daily candidate
    # TODO: Add proper daily challenge logic based on user progress
    import random
    daily_candidates = db.query(Problem).filter(Problem.is_daily_candidate == True).all()
    
    if not daily_candidates:
        raise HTTPException(status_code=404, detail="No daily challenges available")
    
    return random.choice(daily_candidates)