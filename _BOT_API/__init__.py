import telebot
from telebot import types

bot = telebot.TeleBot("5381273626:AAHK8lyq_S1nb_TTxfwaSp8IVKAGe51k_lY")

markup_base = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
item_help = types.KeyboardButton("Список команд")
item_back = types.KeyboardButton("Вернуться в начало")

markup_base.add(item_help, item_back)


help_str =  '/lowprice - Узнать топ самых дешёвых отелей в городе\n\n' \
            '/bestdeal - Узнать топ отелей, наиболее подходящих по цене и количеству звезд\n\n' \
            '/history  - История запросов\n\n' \
            '/historydelete - удалить историю запросов'

