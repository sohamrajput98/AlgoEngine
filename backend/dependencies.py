import os
import jwt
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from db import SessionLocal
from models.user import User

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "secret123")
ALGORITHM = "HS256"

def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Extract current user from JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        # Remove 'Bearer ' prefix if present
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """Ensure current user is admin (you can add admin field to User model later)"""
    # For now, allow all authenticated users to create problems
    # Later you can add: if not current_user.is_admin: raise HTTPException(403, "Admin required")
    return current_user