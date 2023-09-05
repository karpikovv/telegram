from .check import *

help_str = (
    "/lowprice - Узнать топ самых дешёвых отелей в городе\n\n"
    "/bestdeal - Узнать топ отелей, наиболее подходящих по цене и количеству звезд\n\n"
    "/history  - История запросов\n\n"
    "/historydelete - удалить историю запросов"
)


@bot.message_handler(commands=["help"])
def help_bot(message):
    bot.send_message(
        message.chat.id,
        "Бот для поиска подходящих отелей\nСписок команд:\n\n" + help_str,
    )
    get_city(message)
