from enum import Enum
from typing import Tuple, Any, List, Sequence
from sqlalchemy import UUID, select, Row, RowMapping
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from base.models_and_engine import Channel, Video

class Keys(Enum):
    VIEWS = "views"
    AUTHOR = "author"



class HandlerDB:
    model = ...

    def __init__(self, db_session: AsyncSession):
        self._session = db_session

    async def get(self, id: UUID) -> Any:
        channel = await self._session.get(self.model, id)
        return channel

    async def kill(self, id: UUID) -> Tuple[bool,None] | Tuple[bool,str]:
        channel = await self._session.get(self.model, id)
        if channel:
            try:
                await self._session.delete(channel)
                await self._session.commit()
                return True,None
            except IntegrityError as er:
                return False, str(er.orig) + "(Для не программистов, пока не удалите все видео, канал удалить нельзя)"
            except Exception as er:
                return False, f"Unexpected error {er}"

        return False, 'not found'

    async def create(self, **kwargs) -> Tuple[bool, str] | Tuple[Any, None]:
        new_row = self.model(**kwargs)
        self._session.add(new_row)
        try:
            await self._session.flush()
            result = new_row, None
        except IntegrityError as er:
            result = False, f"Integrity Data Error : {er.orig}"
        except Exception as er:
            result = False, f'Unexpected  Error: {str(er)}'
        finally:
            return result

    async def update(self, id: UUID, **kwargs) -> Tuple[DeclarativeBase, None] | Tuple[None, str]:
        result = await self._session.get(self.model, id)
        if not result:
            return None, f'Cannot to execute {self.model.__name__} with id: {id}'
        for key, value in kwargs.items():
            if value:
                setattr(result, str(key), value)
        try:
            await self._session.flush()
            return result, None
        except IntegrityError as er:
            return None, f'Cannot to update data in {self.model.__name__} : {er.orig}'
        except Exception as er:
            return None, f'Unexpected Error {er}'

    async def get_all(self, key: Keys, value: Any = None) -> Sequence[Row | RowMapping | None]:
        """
        Get a list of records from the database.

        :param key: The name of the SQL-model attribute to filter by .
        :param value: The value of the SQL-model attribute to filter by.

        :return: A sequence of rows or None.
        """
        key_value:str = key.value

        if value:
            stmt = select(self.model).where(getattr(self.model, key_value) == value).order_by(getattr(self.model, key_value))
            channels = await self._session.execute(stmt)
        else:
            print("print!!!!!!!!!", self.model,key_value)
            stmt = select(self.model).order_by(getattr(self.model, key_value))
            print(stmt)
            channels = await self._session.execute(stmt)
        result = channels.scalars().all()
        return result


class ChannelsDB(HandlerDB):
    model = Channel


class VideoDB(HandlerDB):
    model = Video
