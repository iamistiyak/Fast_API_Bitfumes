from email.quoprimime import body_check
from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel, DirectoryPath
from typing import List
from blog import models
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .hashing import dcrypt

app = FastAPI()

# Create and migrate a table
models.Base.metadata.create_all(bind=engine)



# Without response body
# @app.post("/blog")
# def blog(title, body):
#     return {"Title":title, "Body": body}
def get_db():
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()     

# Create Blog
@app.post("/createblog", status_code = status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# get all blogs
@app.get("/getblogs", response_model = List[schemas.ShowAllBlog], tags=['blogs'])
def all(db:Session = Depends(get_db)):
  blogs = db.query(models.Blog).all()
  return blogs

# get perticular blogs
@app.get("/blog/{id}", status_code=200, response_model = schemas.ShowBlog, tags=['blogs'])
def show(id, response:Response, db:Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This bolg id {id} is not found")
    #  response.status_code = status.HTTP_404_NOT_FOUND
    #  return {f"This bolg id {id} is not found"}
  return blog


#Delete particular blog 
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id, db:Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This bolg id {id} is not found")
  blog.delete(synchronize_session=False)

  db.commit()
  return {"Done"}
  
#Update particular blog   
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, requests:schemas.Blog, db:Session = Depends(get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This bolg id {id} is not found")
    print(requests)
    blog.update({'title' : requests.title, 'body' :requests.body})  

    db.commit()
    return {"updated"}


# Create User 
@app.post("/user",response_model=schemas.ShowUsers, status_code = status.HTTP_201_CREATED, tags=['users'])
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    
    new_user = models.User(name=request.name, email=request.email, password=dcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user    

# Get particular user
@app.get("/user/{id}",response_model=schemas.ShowUsers, tags=['users'])
def get_user(id: int, db:Session = Depends(get_db)):
    
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"This bolg id {id} is not found")
    #  response.status_code = status.HTTP_404_NOT_FOUND
    #  return {f"This bolg id {id} is not found"}
  return user    