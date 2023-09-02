from .check import *
from _sql_bd_api.bd_get_history import get_history


@bot.message_handler(commands=['history'])
def history(message):
    print(1)
    usr_history = get_history(message.chat.id)
    print(2)
    if not usr_history:
        bot.send_message(message.chat.id, "История запросов пуста")
    else:
        for item in usr_history:
            bot.send_message(message.chat.id,
                             "{}\nОтзывы {}/10 ({})\nЦена за ночь:{}\n{}🌟\nРасстояние до центра: {}\n".format(
                                 item[2],
                                 item[3],
                                 item[4],
                                 item[5],
                                 item[6],
                                 item[7]
                             ), reply_markup=markup_base)
    print(3)
    get_city(message)
