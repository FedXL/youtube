from typing import List
from uuid import UUID


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, constr, model_validator
from sqlalchemy.ext.asyncio import AsyncSession
from base.db_handlers import ChannelsDB, Keys
from base.models_and_engine import get_async_session

channel_router = APIRouter()


class ChannelModel(BaseModel):
    id: UUID
    name: constr(max_length=64)
    author: constr(max_length=64)
    address: constr(max_length=128)


class ChannelsReturnModel(BaseModel):
    channels: List[ChannelModel]


class ChannelsCreate(BaseModel):
    name: constr(max_length=64)
    author: constr(max_length=64)
    address: constr(max_length=128)


class ChannelsRead(BaseModel):
    id: UUID


class ChannelsUpdate(BaseModel):
    id: UUID
    name: constr(max_length=64) = None
    author: constr(max_length=64) = None
    address: constr(max_length=128) = None

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'ChannelsUpdate':
        count = 0
        if self.name:
            count += 1
        if self.author:
            count += 1
        if self.address:
            count += 1
        if count == 0:
            raise ValueError('at list one fields ["name","author","address"] should required')
        return self

class ChannelsList(BaseModel):
    author: constr(max_length=64)


class ResponseDetails(BaseModel):
    details: str


@channel_router.post("/create", tags=['channel operations'], status_code=201,
                     responses={
                         201: {"model": ChannelModel, "description": "Channel was successfully created"},
                         404:{"description":"cannot create channel with that data"}
                     }

                  )
async def create_channel(data: ChannelsCreate, session: AsyncSession = Depends(get_async_session)):
    channel, comment = await ChannelsDB(session).create(author=data.author,
                                               address=data.address,
                                               name=data.name)
    if channel:
        dict_instance = channel.to_dict()
        return ChannelModel(**dict_instance)
    else:
        context = f"cant to create item with that data : {comment}"
        raise HTTPException(status_code=404, detail=context)


@channel_router.post("/read", tags=['channel operations'], responses={
    200: {"model": ChannelModel, "description": "Channel was successfully find"},
    404: { "description": "Cannot to find channel"}
}
                     )
async def read_channel(data: ChannelsRead, session: AsyncSession = Depends(get_async_session)):
    channel = await ChannelsDB(session).get(id=data.id)
    if channel:
        content = ChannelModel(**channel.to_dict())
        return content
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@channel_router.post('/update', tags=['channel operations'], status_code=201, responses={
    201: {"model": ChannelModel, "description": "Channel was successfully updated"},
    404: {"model": ResponseDetails, "description": "Cannot to update channel for a reason"}
})
async def read_channel(data: ChannelsUpdate, session: AsyncSession = Depends(get_async_session)):
    channel, comment = await ChannelsDB(session).update(id=data.id, name=data.name,
                                                        author=data.author, address=data.address)

    if channel:
        content = ChannelModel(**channel.to_dict())
        return content
    else:
        raise HTTPException(status_code=404, detail=comment)


@channel_router.post('/delete', tags=['channel operations'], status_code=204, responses={
    204: {"description": "Channel was successfully deleted"},
    404: {"description": "Cannot to delete channel for a reason"}
})
async def kill_channel(data: ChannelsRead, session: AsyncSession = Depends(get_async_session)):
    result, comment = await ChannelsDB(db_session=session).kill(id=data.id)
    if result:
        return
    raise HTTPException(status_code=404, detail=comment)


@channel_router.post('/list', tags=['channel operations'],
                     responses={
                         200: {"model": ChannelsReturnModel, "description": "Channels author list"},
                         404: {"description": "Cannot to find this author in DB"}}
                     )
async def read_channels(data: ChannelsList, session: AsyncSession = Depends(get_async_session)):
    result = await ChannelsDB(db_session=session).get_all(key=Keys.AUTHOR, value=data.author)
    if not result:
        return HTTPException(status_code=404, detail=f"cant to find this author ")
    context = ChannelsReturnModel(channels=[ChannelModel(**channel.to_dict()) for channel in result])
    return context


@channel_router.get('/list', tags=['channel operations'], response_model=ChannelsReturnModel)
async def read_channels_all(session: AsyncSession = Depends(get_async_session)):
    result = await ChannelsDB(session).get_all(Keys.AUTHOR)
    context = ChannelsReturnModel(channels=[ChannelModel(**channel.to_dict()) for channel in result])
    return context
