from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class TagsRequest(BaseModel):
    text: str


class TagsResponse(BaseModel):
    response: list[str]


class RecognizeSourceType(Enum):
    YOUTUBE = 'youtube'


class RecognizeRequest(BaseModel):
    url: str
    type: RecognizeSourceType


class RecognizeResponse(BaseModel):
    response: str


@router.post('/recognition/tags', response_model=TagsResponse)
async def get_tags(text: TagsRequest):
    return TagsResponse(response=text.text.split())


@router.post('/recognition/recognize', response_model=RecognizeResponse)
async def get_recognize(data: RecognizeRequest):
    return RecognizeResponse(response="")
