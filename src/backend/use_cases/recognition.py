from __future__ import annotations

import os
import re
from datetime import timedelta

import yt_dlp as youtube_dl

from backend.repositories.record_repository import RecordRepository
from ml import recognize, tags

from .recognition_dto import (
    RecognizeRequest,
    RecognizeResponse,
    RecognizeSourceType,
    Segment,
    TagsRequest,
    TagsResponse,
)


class TagsUseCase:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    async def execute(self, data: TagsRequest) -> TagsResponse:
        text_tags = tags.get(data.text)

        author_tags = []
        if data.video_id:
            record = await self.record_repository.findByVideoInfoId(data.video_id)
            if record:
                author_tags = record['video_info'].get('author_tags')

        return TagsResponse(tags=text_tags, author_tags=author_tags)


def get_video_id(url: str) -> str:
    return re.search(r"v=([A-Za-z0-9_-]+)", url).group(1)


def download_audio(url: str) -> dict:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }
        ],
        'verbose': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_filename = ydl.prepare_filename(info_dict)
    if not audio_filename.endswith('.wav'):
        extension = audio_filename.split('.')[-1]
        audio_filename = audio_filename.replace(extension, 'wav')
    return {
        "id": info_dict["id"],  # type: ignore
        "title": info_dict["title"],  # type: ignore
        "channel": info_dict["channel"],  # type: ignore
        "duration": info_dict["duration"],  # type: ignore
        "url": info_dict["original_url"],  # type: ignore
        "author_tags": info_dict["tags"],  # type: ignore
        "audio_filename": audio_filename,
    }


class RecordMapping:
    def to_time_code(self, seconds: int) -> str:
        res = str(timedelta(seconds=seconds))
        res = res.split('.')[0]
        return res

    def from_dict(self, data: dict):
        return RecognizeResponse(
            text=data['text'],
            segments=list(
                map(
                    lambda x: Segment(
                        text=x['text'],
                        start=x['start'],
                        end=x['end'],
                        slug_time=f'{self.to_time_code(seconds=x["start"])} - {self.to_time_code(seconds=x["end"])}',
                    ),
                    data['segments'],
                )
            ),
        )


class RecognizeUseCase:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    async def execute(self, data: RecognizeRequest) -> RecognizeResponse:
        if data.type == RecognizeSourceType.YOUTUBE:
            result = await self.record_repository.findByVideoInfoUrl(data.url)
            if result:
                return RecordMapping().from_dict(result)

            if self.record_repository.is_lock(get_video_id(data.url)):
                raise Exception("Queue is locked, please try again later")
            video_info = download_audio(data.url)

            result = await self.record_repository.findByVideoInfoId(video_info['id'])
            if result:
                return RecordMapping().from_dict(result)

            await self.record_repository.lock(video_info['id'])
            audio_filename = video_info['audio_filename']
            result = recognize.get(audio_filename)

            if os.path.isfile(audio_filename):
                os.remove(audio_filename)

            result.setdefault('record_type', data.type.value)
            result.setdefault('video_info', video_info)

            await self.record_repository.create(result)
            await self.record_repository.unlock(video_info['id'])
            return RecordMapping().from_dict(result)
        raise NotImplementedError
