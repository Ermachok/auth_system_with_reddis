from fastapi import Depends, Header, HTTPException, Request

from app.redis_client import redis_client
from app.utils.auth import decode_token


def verify_token(request: Request, authorization: str = Header(None)):
    token = None
    if authorization:
        token = authorization.split(" ")[1] if " " in authorization else authorization
    else:

        token_cookie = request.cookies.get("access_token")
        if token_cookie:
            token = token_cookie.split(" ")[1] if " " in token_cookie else token_cookie

    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")

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
