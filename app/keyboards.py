from aiogram.types import (InlineKeyboardMarkup, ReplyKeyboardMarkup, 
                           InlineKeyboardButton, KeyboardButton)


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Github repo', url='https://github.com/Curiod/momoechi_bot')],
    [InlineKeyboardButton(text='QA mode on', callback_data='QA')],
    [InlineKeyboardButton(text='Contacts', callback_data='contacts')]
]
)

qa_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='QA mode off'),
    KeyboardButton(text='Short description')]],
                                    resize_keyboard=True)

    
    
