from fastapi import APIRouter, Depends, HTTPException

from backend.repositories.record_repository import RecordRepository
from backend.use_cases.recognition import RecognizeUseCase, TagsUseCase
from backend.use_cases.recognition_dto import RecognizeRequest, RecognizeResponse, TagsRequest, TagsResponse

router = APIRouter()


@router.post('/recognition/tags', response_model=TagsResponse)
async def get_tags(data: TagsRequest, repo: RecordRepository = Depends(RecordRepository)):
    if len(data.text.split()) < 10:
        raise HTTPException(status_code=400, detail="Text too short")
    return await TagsUseCase(repo).execute(data)


@router.post('/recognition/recognize', response_model=RecognizeResponse)
async def get_recognize(data: RecognizeRequest, repo: RecordRepository = Depends(RecordRepository)):
    try:
        return await RecognizeUseCase(repo).execute(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
