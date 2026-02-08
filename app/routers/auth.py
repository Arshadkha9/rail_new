from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken
from app.core.jwt import create_refresh_token, refresh_token_expiry
from app.db.session import get_db
from app.models.user import User
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.deps import get_current_user
from datetime import datetime
from fastapi import Request
from app.core.limiter import limiter


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
@limiter.limit("3/minute")
def register(request: Request,email: str, password: str, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email
    }


@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request,email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})

    refresh_token = create_refresh_token()

    rt = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=refresh_token_expiry()
    )

    db.add(rt)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }

@router.post("/refresh")
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    rt = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token)
        .first()
    )

    if not rt or rt.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(
        {"sub": str(rt.user_id)}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
