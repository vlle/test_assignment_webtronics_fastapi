from crud import get_user_by_login
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from models import Robot
from passlib.context import CryptContext
from pydantic_models import RobotLoginForm
from sqlalchemy.ext.asyncio import AsyncSession

# random 128 letter key for jwt key
KEY = "c537dc83a4d4b8b0d8138122b53a86f341f6bb60e23174d940aa7e7d3dfecbda"
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(db: AsyncSession, user: RobotLoginForm) -> Robot | None:
    db_user = await get_user_by_login(db, user.login)
    if not db_user:
        return None
    is_password_correct = verify_password(user.password, db_user.password)
    if not is_password_correct:
        return None
    return db_user


async def has_access(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Function that is used to validate the token in the case that it requires it
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            key=KEY,
        )
    except JWTError as e:  # catches any exception
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return payload
