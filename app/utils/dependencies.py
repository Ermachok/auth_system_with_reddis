from auth import decode_token
from fastapi import Depends, Header, HTTPException

from app.redis_client import redis_client


def verify_token(authorization: str = Header(...)):
    token = authorization.split(" ")[1] if " " in authorization else authorization
    if not redis_client.sismember("whitelist", token) or redis_client.sismember(
        "blacklist", token
    ):
        raise HTTPException(status_code=401, detail="Token not allowed")
    return decode_token(token)


def role_required(required_role: str):
    def wrapper(payload: dict = Depends(verify_token)):
        if payload["role"] != required_role:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return payload

    return wrapper
