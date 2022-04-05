from typing import List
from fastapi import APIRouter,Depends,status,HTTPException, Response
from .. import schemas, database, models
from sqlalchemy.orm import Session
# from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

get_db = database.get_db

# @router.post('/', status_code=status.HTTP_201_CREATED,)
# def create(request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return blog.create(request, db)
# Create Blog

@router.post("/", status_code = status.HTTP_201_CREATED)
def create(request: schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# @router.get('/', response_model=List[schemas.ShowBlog])
# def all(db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return blog.get_all(db)
# get all blogs
@router.get("/", response_model = List[schemas.ShowAllBlog])
def all(db:Session = Depends(get_db)):
  blogs = db.query(models.Blog).all()
  return blogs

# @router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
# def show(id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return blog.show(id,db)
# get perticular blogs

@router.get("/{id}", status_code=200, response_model = schemas.ShowAllBlog)
def show(id, response:Response, db:Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This bolg id {id} is not found")
    #  response.status_code = status.HTTP_404_NOT_FOUND
    #  return {f"This bolg id {id} is not found"}
  return blog

# @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def destroy(id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return blog.destroy(id,db)

#Delete particular blog     
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This bolg id {id} is not found")
  blog.delete(synchronize_session=False)
  db.commit()
  return {"Done"}    


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update(id:int, request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return blog.update(id,request, db)
#Update particular blog   

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, requests:schemas.Blog, db:Session = Depends(get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This bolg id {id} is not found")
    print(requests)
    blog.update({'title' : requests.title, 'body' :requests.body})  

    db.commit()
    return {"updated"}

