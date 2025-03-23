from fastapi import FastAPI

from app.routers import web_router

app = FastAPI()

app.include_router(web_router.router)
