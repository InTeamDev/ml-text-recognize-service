from fastapi import APIRouter

from . import recognition

api_router = APIRouter()
api_router.include_router(recognition.router, tags=['Recognition'])
