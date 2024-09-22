from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F

import app.keyboards as kb


router = Router()


class QA_mode(StatesGroup):
    mode = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Hi, {message.from_user.first_name} {message.from_user.last_name}!\n\
                         Select a menu item:',
                         reply_markup=kb.main)


@router.message(F.text =='QA mode off')
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Select a menu item:',
                                  reply_markup=kb.main)
    
    
@router.callback_query(F.data =='QA')
async def QA(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text='Write your question', 
                                  reply_markup=kb.qa_keyboard)
    await state.set_state(QA_mode.mode)
       

@router.message(QA_mode.mode)
async def reply(message: Message):
    await message.reply(text=message.text)


@router.callback_query(F.data =='contacts')
async def contacts(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text='tg: @momoechi \ngmail: tearbender99@gmail.com',
                                  reply_markup=kb.main)
    

@router.message(F.text =='Short description')
async def description(message: Message):
    pass