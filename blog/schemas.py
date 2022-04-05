from pydantic import BaseModel
from typing import Optional, List


class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
          orm_mode = True 


# For response model
class ShowAllBlog(BaseModel):
      title: str
      body: str
      class Config():
          orm_mode = True 


class User(BaseModel):
    name: str
    password: str
    email: str

# For response model
class ShowUsers(BaseModel):
      name: str
      email: str
      blogs:List[Blog]

      class Config():
          orm_mode = True 
          
# For response model
class ShowBlog(BaseModel):
      title: str
      body: str
      id: int
      creator: ShowUsers
      class Config():
          orm_mode = True           