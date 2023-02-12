from sqlalchemy.orm import Session
import models, schemas, hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.CreateUser):
    hashed_password = hash.Hash.bcypt(password=user.password)
    new_user = models.User(
        name = user.name,
        password = hashed_password 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user