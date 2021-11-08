from jose import JWTError, jwt
from datetime import datetime, timedelta

#SECRET_KEY
#Algorithm
#Expiration Time

SECRET_KEY = "w8jjahde66ubepigscm2swvuxw3x78xmwwc4pu25rct95e2mg4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt