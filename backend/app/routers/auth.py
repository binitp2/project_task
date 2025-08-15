from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserLogin, UserOut, Token
from ..security import verify_password, get_password_hash, create_access_token
from ..database import get_db_session
from ..models import User

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate, db: Session = Depends(get_db_session)):
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    except ValueError as e:
        # Handle Pydantic validation errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db_session)):
    # Find user by email
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user_data.email})
    
    return Token(access_token=access_token, token_type="bearer")


