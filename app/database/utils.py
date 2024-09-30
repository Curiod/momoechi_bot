import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.database.models import Base

load_dotenv()

engine = create_async_engine(url=os.getenv('SQL_ALCHEMY_URL'))

session_maker  = async_sessionmaker(engine)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        
async def get_default_session():
    async with session_maker() as session:
        return session