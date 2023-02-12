from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.param_functions import Depends as authDepends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import engine
import crud, models, schemas, oauth2, hash, database

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(
    user_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user)):
    return crud.get_user(db, user_id)

@app.get("/users2/{user_id}", response_model=schemas.User)
def get_user2(
    user_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user),
    Authorization: str = Header(default=None)):
    return crud.get_user(db, user_id)


@app.post("/users/", response_model=schemas.CreateUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/token")
def get_token(request: OAuth2PasswordRequestForm = authDepends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.name == request.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credentials'
        )
    if not hash.Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect password'
        )
    
    access_token = oauth2.create_access_token(data={"sub": user.name})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "user_name": user.name
    }
