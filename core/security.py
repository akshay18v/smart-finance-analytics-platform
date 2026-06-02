from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password:str)->str:
    """takes a raw password string and returns a secure,unreadable hash."""
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    """checks if the input password matches stored database hash."""
    return pwd_context.verify(plain_password,hashed_password)