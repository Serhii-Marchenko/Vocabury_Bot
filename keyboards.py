from aiogram import types

markup_buttons_save = types.InlineKeyboardMarkup()
but_yes = types.InlineKeyboardButton("Cохранить в словарь",callback_data='translationfromenglish')
but_no = types.InlineKeyboardButton("Продолжить без сохранения",callback_data='translationtoenglish')
markup_buttons_save.add(but_yes, but_no)
