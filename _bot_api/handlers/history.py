from _sql_bd_api.bd_get_history import get_history

from .check import *


@bot.message_handler(commands=["history"])
def history(message):
    usr_history = get_history(message.chat.id)
    if not usr_history:
        bot.send_message(message.chat.id, "История запросов пуста")
    else:
        for item in usr_history:
            bot.send_message(
                message.chat.id,
                "{}\nОтзывы {}/10 ({})\nЦена за ночь:{}\n{}🌟\nРасстояние до центра: {}\n".format(
                    item[2], item[3], item[4], item[5], item[6], item[7]
                ),
                reply_markup=markup_base,
            )
    get_city(message)
