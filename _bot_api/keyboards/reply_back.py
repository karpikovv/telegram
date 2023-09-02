from telebot import types


markup_base = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
item_help = types.KeyboardButton("Список команд")
item_back = types.KeyboardButton("Вернуться в начало")

markup_base.add(item_help, item_back)
