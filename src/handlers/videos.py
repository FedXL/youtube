from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, constr, model_validator
from base.db_handlers import VideoDB, Keys
from base.models_and_engine import get_async_session

video_router = APIRouter()


class GetVideoID(BaseModel):
    id: UUID


class GetVideoViews(BaseModel):
    views: int


class CreateVideo(GetVideoViews):
    title: constr(max_length=64)
    channel: UUID


class VideoModel(CreateVideo, GetVideoID):
    pass


class ListVideoModel(BaseModel):
    videos: List[VideoModel]


class UpdateVideo(BaseModel):
    id: UUID
    views: int = None
    title: constr(max_length=64)=None
    channel: UUID = None

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UpdateVideo':
        count = 0
        if self.title:
            count += 1
        if self.views:
            count += 1
        if self.channel:
            count += 1
        if count == 0:
            raise ValueError('at list one fields ["title","views","channel"] should required')
        return self


@video_router.post("/create", tags=['videos operations'],
                   status_code=201, response_model=VideoModel,
                   responses={404: {"description": "cannot create video with that data"}})
async def create_video(data: CreateVideo, session=Depends(get_async_session)):
    print(data)
    video, comment = await VideoDB(session).create(**data.model_dump())
    if video:
        return VideoModel(**video.to_dict())
    else:
        raise HTTPException(status_code=404, detail=comment)


@video_router.post("/read", tags=['videos operations'], response_model=VideoModel,
                   responses={404: {"description": "no video"}})
async def read_one_video(data: GetVideoID, session=Depends(get_async_session)):
    video = await VideoDB(session).get(data.id)
    if video:
        return VideoModel(**video.to_dict())
    raise HTTPException(status_code=404, detail="cant to find video")


@video_router.post('/update', tags=['videos operations'], response_model=VideoModel,
                   responses={404: {"description": "no video"}})
async def update_video(data: UpdateVideo, session=Depends(get_async_session)):
    video, comment = await VideoDB(session).update(**data.model_dump())
    if video:
        return VideoModel(**video.to_dict())
    raise HTTPException(status_code=404, detail=comment)


@video_router.post('/delete', tags=['videos operations'], status_code=204,
                   responses={404: {"description": "no video"}})
async def delete_video(data: GetVideoID, session=Depends(get_async_session)):
    result, comment = await VideoDB(session).kill(**data.model_dump())
    if result:
        return
    raise HTTPException(status_code=404, detail=comment)


@video_router.post('/list', tags=['videos operations'] ,response_model=ListVideoModel,
                   responses={404: {"description": "no video"}})
async def get_video_by_views(data: GetVideoViews, session=Depends(get_async_session)):
    result = await VideoDB(session).get_all(key=Keys.VIEWS, value=data.views)
    if result:
        return ListVideoModel(videos=[VideoModel(**video.to_dict()) for video in result])
    else:
        HTTPException(status_code=404,detail="cant to get list")

@video_router.get('/list',tags=['videos operations'],response_model=ListVideoModel, responses={404: {"description": "no video"}})
async def get_video_all(session=Depends(get_async_session)):
    result = await VideoDB(session).get_all(key=Keys.VIEWS)
    if result:
        return ListVideoModel(videos=[VideoModel(**video.to_dict()) for video in result])
    else:
        HTTPException(status_code=404,detail="cant to get list")
