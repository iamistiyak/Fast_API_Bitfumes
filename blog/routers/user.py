from fastapi import APIRouter, HTTPException
from .. import database, schemas, models
from ..hashing import dcrypt
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status
# from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


# @router.post('/', response_model=schemas.ShowUser)
# def create_user(request: schemas.User,db: Session = Depends(get_db)):
#     return user.create(request,db)
# Create User 
@router.post("/",response_model=schemas.ShowUsers, status_code = status.HTTP_201_CREATED)
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    
    new_user = models.User(name=request.name, email=request.email, password=dcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user     


# @router.get('/{id}',response_model=schemas.ShowUser)
# def get_user(id:int,db: Session = Depends(get_db)):
#     return user.show(id,db)

# Get particular user
@router.get("/{id}",response_model=schemas.ShowUsers)
def get_user(id: int, db:Session = Depends(get_db)):
    
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This user id {id} is not found")
    #  response.status_code = status.HTTP_404_NOT_FOUND
    #  return {f"This bolg id {id} is not found"}
  return user 