from fastapi import APIRouter, HTTPException

from backend.use_cases.recognition import RecognizeUseCase, TagsUseCase
from backend.use_cases.recognition_dto import RecognizeRequest, RecognizeResponse, TagsRequest, TagsResponse

router = APIRouter()


@router.post('/recognition/tags', response_model=TagsResponse)
async def get_tags(data: TagsRequest):
    if len(data.text.split()) < 10:
        raise HTTPException(status_code=400, detail="Text too short")
    return TagsUseCase().execute(data)


@router.post('/recognition/recognize', response_model=RecognizeResponse)
async def get_recognize(data: RecognizeRequest):
    return RecognizeUseCase().execute(data)
