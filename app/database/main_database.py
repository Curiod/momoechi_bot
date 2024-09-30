import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Document, User

from whoosh.writing import AsyncWriter

import os
from os.path import dirname
from dotenv import load_dotenv

from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.index import create_in, open_dir, exists_in



from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.database.models import Base

load_dotenv()

engine = create_async_engine(url=os.getenv('SQL_ALCHEMY_URL'))
session_maker  = async_sessionmaker(engine)

class DataRepository:
    def __init__(self):
        schema = Schema(
            id=NUMERIC(stored=True),  
            content=TEXT(stored=False)
        )
        index_dir = os.path.join(dirname(dirname(dirname(__file__))), 'data')
        index_dir = os.path.join(index_dir, 'whoosh_index')

        if exists_in(index_dir):
            self.ix = open_dir(index_dir)

        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
            self.ix = create_in(index_dir, schema)
        

    async def get_contexts(self):
        async with session_maker() as session:
            return await session.scalars(select(Document))
    

    async def set_user(self, tg_id: int) -> None:
        async with session_maker() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            if not user:
                session.add(User(tg_id=tg_id))
                await session.commit()


    async def add_documents(self, df: pd.DataFrame):
        writer = AsyncWriter(self.ix)
        documents = []
        async with session_maker() as session:
            for _, row in df.iterrows():
                doc_instance = Document(content=row['context'])
                documents.append(doc_instance)

            session.add_all(documents)
            await session.flush()    

            for doc_instance, prep_doc in zip(documents, df['preprocessed']):
                doc_id = doc_instance.id
                writer.add_document(id=doc_id, content=prep_doc)

            await session.commit()
            writer.commit()


    def get_index(self):
        return self.ix

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)