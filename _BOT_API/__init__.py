import telebot
from telebot import types

bot = telebot.TeleBot("5381273626:AAHK8lyq_S1nb_TTxfwaSp8IVKAGe51k_lY")

markup_base = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
item_help = types.KeyboardButton("Список команд")
item_back = types.KeyboardButton("Вернуться в начало")

markup_base.add(item_help, item_back)