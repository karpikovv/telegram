from .check import *
from _sql_bd_api.bd_delete_history import delete_history


@bot.message_handler(commands=['historydelete'])
def history_delete(message):
    delete_history(message.chat.id)
    bot.send_message(message.chat.id, "История запросов успешно удалена\n")
    get_city(message)
