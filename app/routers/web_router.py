from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.redis_client import redis_client
from app.utils.auth import create_token
from app.utils.dependencies import verify_token

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


@router.get("/debug/")
def debug_form(request: Request):
    return templates.TemplateResponse("debug.html", {"request": request})


@router.post("/debug/")
def debug_add(request: Request, username: str = Form(...), role: str = Form(...)):
    token = create_token(username=username, role=role)
    return templates.TemplateResponse(
        "debug.html", {"request": request, "token": token}
    )


@router.get("/login/")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login/")
def login_user(request: Request, username: str = Form(...), role: str = Form(...)):
    token = create_token(username=username, role=role)
    response = RedirectResponse(url="/content/", status_code=302)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return response


@router.get("/content/")
def content(request: Request, user=Depends(verify_token)):
    return templates.TemplateResponse(
        "content.html",
        {"request": request, "username": user["sub"], "role": user["role"]},
    )


@router.post("/logout/")
def logout(request: Request):
    token = request.cookies.get("access_token")
    if token:
        token_value = token.split(" ")[1] if " " in token else token
        redis_client.srem("whitelist", token_value)
        redis_client.sadd("blacklist", token_value)
    response = RedirectResponse(url="/login/", status_code=302)
    response.delete_cookie("access_token")
    return response
