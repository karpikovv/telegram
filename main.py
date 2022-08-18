import telebot
from telebot import types

bot = telebot.TeleBot("5381273626:AAHK8lyq_S1nb_TTxfwaSp8IVKAGe51k_lY")


'''Список реализованных команд для бота'''
help_str = '/lowprice - Узнать топ самых дешёвых отелей в городе\n\n' \
           '/highprice - Узнать топ самых дорогих отелей в городе\n\n' \
           '/bestdeal - Узнать топ отелей, наиболее подходящих по цене и расположению от центра\n\n' \
           '/history - Узнать историю поиска отелей\n\n'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Func Start")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_low = types.KeyboardButton("Топ Дешевых")
    item_high = types.KeyboardButton("Топ дорогих")
    item_choice = types.KeyboardButton("Подобрать подходящий")
    markup.add(item_low, item_high, item_choice)
    bot.send_message(message.chat.id, 'q', reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Бот для поиска подходящих отелей\nСписок команд:\n\n' + help_str)


@bot.message_handler(commands=['lowprice'])
def low(message):
    bot.reply_to(message, "Func lowprice")


@bot.message_handler(commands=['highprice'])
def high(message):
    bot.reply_to(message, "Func highprice")


@bot.message_handler(commands=['bestdeal'])
def best_deal(message):
    bot.reply_to(message, "Func bestdeal")


@bot.message_handler(commands=['history'])
def history(message):
    bot.reply_to(message, "Func history")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Топ Дешевых':
        low(message)
    elif message.text == "Топ дорогих":
        high(message)
    elif message.text == "Подобрать подходящий":
        best_deal(message)
    else:
        bot.send_message(message.chat.id, 'Неизвестная команда, список команд - /help')
    print(message)
    print(message.text)


bot.infinity_polling()
