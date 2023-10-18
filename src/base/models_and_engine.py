import asyncio
import uuid
from typing import AsyncGenerator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from base.config import DB_URL

async_engine = create_async_engine(DB_URL, echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    print("session starts")
    async with async_session_maker() as session:
        async with session.begin():
            yield session


class Base(DeclarativeBase):
    pass


class Channel(Base):
    __tablename__ = 'channels'
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = mapped_column(String(length=64), unique=True)
    author = mapped_column(String(length=64))
    address = mapped_column(String(length=128), unique=True)

    def __repr__(self):
        return f"id = {self.id} | name = {self.name} | author = {self.author} | address = {self.address[:20]}"

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'author': self.author,
            'address': self.address
        }


class Video(Base):
    __tablename__ = 'videos'
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = mapped_column(String(length=64), name='Title', unique=True)
    views = mapped_column(Integer)
    channel = mapped_column(ForeignKey("channels.id"))

    def __repr__(self):
        return f"id = {self.id} | title = {self.title} | views = {self.views} | address = {self.channel}"

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'views': self.views,
            'channel': self.channel
        }



async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



