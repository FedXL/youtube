import asyncio

from base.models_and_engine import create_tables

if __name__ == "__main__":
    asyncio.run(create_tables())