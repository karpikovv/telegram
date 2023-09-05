from telebot import types

markup_bool = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
item_yes = types.KeyboardButton("Да")
item_no = types.KeyboardButton("Нет")

markup_bool.add(item_yes, item_no)
