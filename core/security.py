import jwt
from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
#SECRET KEY TO SIGN YOUR TOKENS (KEEP THIS PRIVATE!)
SECRET_KEY="SUPER_SECRET_PLATFORM_KEY_CHANGE_THIS_LATER"
#CRYPTOGRAPHIC ALGORITHM TO SIGN THE TOKEN
ALGORITHM="HS256"
#HOW LONG THE LOGIN BADGE STAYS VALID BEFORE EXPIRING
ACCESS_TOKEN_EXPIRE_MINUTES=30


def get_password_hash(password:str)->str:
    """takes a raw password string and returns a secure,unreadable hash."""
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    """checks if the input password matches stored database hash."""
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict)-> str:
    """Generates a secure,signed JWT token string containing user data"""
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
