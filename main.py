from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Query parameters 
@app.get("/blog")
def blog(limit, published : bool = True, sort : Optional[str] = "Optional"):
    return {f'Blog limit is {limit} and {published} and {sort}'}    

@app.get("/")
def index():
    return {"Hello": {"Country" : "Canada"}}


@app.get("/about")
def about():
    return {"About":"About"}

# Path parameter
@app.get('/blog/{id}')
def show(id : int):
    return {"id" : id}    

@app.get("/blog/{id}/comments")
def comments(id):
    return {"comments id" : {
        "id": id,
        "Comment": "First comment"
    }}    


# body request
class Blog(BaseModel):
    title: str = "First blog"
    body: str
    published: Optional[bool] = False
   

@app.post("/blogpost")
def blog(blog: Blog):
    return {f"Blog is published as {blog.title}"}   
               








