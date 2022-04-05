from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def dcrypt(password: str):
    return pwd_context.hash(password)