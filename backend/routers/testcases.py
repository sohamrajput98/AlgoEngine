from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_admin_user, get_current_user
from models.problem import Problem
from models.testcase import TestCase
from schemas.testcases import TestCaseCreate, TestCaseResponse, TestCasePublicResponse, TestCaseUpdate

router = APIRouter(prefix="/problems", tags=["testcases"])

@router.post("/{problem_id}/testcases", response_model=TestCaseResponse)
def create_testcase(
    problem_id: int,
    testcase: TestCaseCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    """Create a new testcase for a problem (admin only)"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    db_testcase = TestCase(problem_id=problem_id, **testcase.dict())
    db.add(db_testcase)
    db.commit()
    db.refresh(db_testcase)
    return db_testcase

@router.get("/{problem_id}/testcases", response_model=list[TestCasePublicResponse])
def get_problem_testcases(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get testcases for a problem (hides expected output for non-sample cases)"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    testcases = db.query(TestCase).filter(TestCase.problem_id == problem_id).all()
    
    # Convert to public response format
    public_testcases = []
    for tc in testcases:
        public_tc = TestCasePublicResponse(
            id=tc.id,
            problem_id=tc.problem_id,
            input_data=tc.input_data,
            is_sample=tc.is_sample,
            expected_output=tc.expected_output if tc.is_sample else None
        )
        public_testcases.append(public_tc)
    
    return public_testcases

@router.get("/{problem_id}/testcases/admin", response_model=list[TestCaseResponse])
def get_problem_testcases_admin(
    problem_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    """Get all testcases for a problem with expected outputs (admin only)"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    return db.query(TestCase).filter(TestCase.problem_id == problem_id).all()

@router.get("/testcases/{testcase_id}", response_model=TestCaseResponse)
def get_testcase(
    testcase_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    """Get a single testcase by ID (admin only)"""
    testcase = db.query(TestCase).filter(TestCase.id == testcase_id).first()
    if not testcase:
        raise HTTPException(status_code=404, detail="TestCase not found")
    return testcase

@router.put("/testcases/{testcase_id}", response_model=TestCaseResponse)
def update_testcase(
    testcase_id: int,
    testcase_update: TestCaseUpdate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    """Update a testcase (admin only)"""
    testcase = db.query(TestCase).filter(TestCase.id == testcase_id).first()
    if not testcase:
        raise HTTPException(status_code=404, detail="TestCase not found")
    
    for field, value in testcase_update.dict(exclude_unset=True).items():
        setattr(testcase, field, value)
    
    db.commit()
    db.refresh(testcase)
    return testcase

@router.delete("/testcases/{testcase_id}")
def delete_testcase(
    testcase_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    """Delete a testcase (admin only)"""
    testcase = db.query(TestCase).filter(TestCase.id == testcase_id).first()
    if not testcase:
        raise HTTPException(status_code=404, detail="TestCase not found")
    
    db.delete(testcase)
    db.commit()
    return {"message": "TestCase deleted successfully"}