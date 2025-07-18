from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app_models import User
from users.schemas import UserCreate, UserOut
import hashlib

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user after validating uniqueness of email and username.
    Password is hashed using SHA-256 before saving.
    """
    if db.query(User).filter(User.user_name == user.user_name).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        user_name = user.user_name, 
        email = user.email, 
        full_name = user.full_name,
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    """
    Retrieve and return a list of all registered users.
    """
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by their unique ID.
    Raise 404 if not found.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user