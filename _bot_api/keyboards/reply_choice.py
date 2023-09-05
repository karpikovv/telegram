from telebot import types

markup_choice = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

item_low = types.KeyboardButton("Топ дешевых")
item_choice = types.KeyboardButton("Подобрать подходящий")
item_back = types.KeyboardButton("Вернуться в начало")

markup_choice.add(item_low, item_choice, item_back)
