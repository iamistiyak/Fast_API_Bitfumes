from typing import List
from fastapi import APIRouter,Depends,status,HTTPException, Response
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)


get_db = database.get_db

# Create Blog
@router.post('/', status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


# get all blogs
@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)

# get perticular blogs
@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id:int, db: Session = Depends(get_db)):
    return blog.show(id,db)


#Delete particular blog  
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return blog.destroy(id,db)
      

# Update particular blog 
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id,request, db)
  

# @router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
# def update(id, requests:schemas.Blog, db:Session = Depends(get_db)):
#     blog =  db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This bolg id {id} is not found")
#     print(requests)
#     blog.update({'title' : requests.title, 'body' :requests.body})  

#     db.commit()
#     return {"updated"}

