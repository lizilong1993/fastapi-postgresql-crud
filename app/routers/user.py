from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter()


@router.get('/me', response_model=schemas.UserResponse)
def get_me(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


@router.put('/updateMe')
async def update_me(payload: schemas.UserBaseSchema, db: Session = Depends(get_db),
                    user_id: str = Depends(oauth2.require_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    name = payload.name
    email = payload.email
    photo = payload.photo
    if user.name == name and user.email == email:
        return {'message': 'Name or Email is the same'}
    else:
        user.name = name
        user.email = email
        user.photo = photo
        db.commit()
        db.refresh(user)
        return {'message': 'User info updated successfully'}
