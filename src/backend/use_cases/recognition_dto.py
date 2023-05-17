from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TagsRequest(BaseModel):
    text: str
    video_id: Optional[str]


class TagsResponse(BaseModel):
    tags: list[str]
    author_tags: list[str]


class RecognizeSourceType(Enum):
    YOUTUBE = 'youtube'


class RecognizeRequest(BaseModel):
    url: str
    type: RecognizeSourceType


class Segment(BaseModel):
    text: str
    start: int
    end: int
    slug_time: str


class RecognizeResponse(BaseModel):
    text: str
    segments: list[Segment]
