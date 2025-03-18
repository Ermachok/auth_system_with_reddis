import datetime

import jwt
from fastapi import HTTPException

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from app.redis_client import redis_client


def create_token(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.datetime.now()
        + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    redis_client.sadd("whitelist", token)
    return token


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
