import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.base.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, TEST_DB_NAME
from src.base.models_and_engine import Base, get_async_session, Channel
from src.main import app

DB_URL_TEST = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}'
async_engine_test = create_async_engine(DB_URL_TEST, echo=True)
Base.metadata.bind = async_engine_test


async def get_async_session_test():
    async with AsyncSession(async_engine_test) as session:
        async with session.begin():
            yield session


app.dependency_overrides[get_async_session] = get_async_session_test





@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def async_client():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
