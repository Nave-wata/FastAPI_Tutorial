from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.CreateUser):
    db_user = models.User(
        name = user.name,
        age = user.age
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
