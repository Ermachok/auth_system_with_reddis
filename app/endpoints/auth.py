from fastapi import APIRouter, Depends

from app.redis_client import redis_client
from app.utils.auth import create_token, decode_token
from app.utils.dependencies import role_required, verify_token

router = APIRouter(prefix="api/")


@router.post("/login/")
def login(username: str, role: str):
    token = create_token(username, role)
    return {"access_token": token}


@router.post("/logout/")
def logout(token: str):
    redis_client.srem("whitelist", token)
    redis_client.sadd("blacklist", token)
    return {"message": "Logged out"}


@router.get("/admin/")
def admin_content(user=Depends(role_required("admin"))):
    return {"message": f"Hello, admin {user['sub']}"}


@router.get("/user/")
def user_content(user=Depends(role_required("user"))):
    return {"message": f"Hello, user {user['sub']}"}
