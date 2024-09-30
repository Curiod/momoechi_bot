import asyncio
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F

import app.keyboards as kb

from app.database.main_database import DataRepository
from app.database.utils import get_default_session
from app.nlp.document_retrieval import search_document
from app.nlp.preprocessing import preprocess_text


router = Router()
mdb = DataRepository()
ix = mdb.get_index()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await mdb.set_user(message.from_user.id)
    await message.answer(f'Hi, {message.from_user.first_name} {message.from_user.last_name}!\n\
                         Select a menu item or ask a question:',
                         reply_markup=kb.main)
       

@router.message(F.text)
async def reply(message: Message):
    """
        Replies to user's question
    """
    query_str = preprocess_text([message.text])[0]  
    result = await search_document(ix, query_str)
    response = str(result) if result else "Документ не найден."

    await message.reply(text=response)


@router.callback_query(F.data =='contacts')
async def contacts(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text='tg: @momoechi \ngmail: tearbender99@gmail.com',
                                  reply_markup=kb.main)
    

@router.message(F.data =='description')
async def description(message: Message):
    pass