from aiogram.types import (InlineKeyboardMarkup, 
                           InlineKeyboardButton)


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Github repo', url='https://github.com/Curiod/momoechi_bot')],
    [InlineKeyboardButton(text='Short description', callback_data='description')],
    [InlineKeyboardButton(text='Contacts', callback_data='contacts')]
]
)


    
    
