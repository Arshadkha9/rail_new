# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# from sqlalchemy.orm import Session

# from app.db.session import get_db
# from app.models.user import User
# from app.core.jwt import SECRET_KEY, ALGORITHM

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db),
# ):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str | None = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     user = db.query(User).filter(User.id == int(user_id)).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user



from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.jwt import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
