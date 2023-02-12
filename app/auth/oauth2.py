from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
import database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "5249dfec52b35a90c73343f548c79618d2b9ef420137acb1936f800664398193"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Colud not validate credentials',
        headers={'WWW-Authenticate': "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

def get_user_by_username(db: Session, name: str):
    user = db.query(models.User).filter(models.User.name == name).first()
    if not name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with name {name} not found')
    return user