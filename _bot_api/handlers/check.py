from loader import bot
import _bot_api.handlers as func
from ..keyboards.reply_back import markup_base


@bot.message_handler(content_types=["text"])
def check_command(message, destination_id=0, count_print=0, photo_fl=False):
    if message.text in ("Вернуться в начало", "/back", "/start"):
        func.start.send_welcome(message)
        return 1
    elif message.text in ("Список команд", "/help"):
        func.help.help_bot(message)
        return 1
    elif message.text == "/history":
        func.history.history(message)
        return 1
    elif message.text == "/historydelete":
        func.historydelete.history_delete(message)
        return 1
    elif destination_id and count_print:
        if message.text == 'Топ дешевых':
            func.low_price.low(message, destination_id, count_print, photo_fl)
        elif message.text == "Подобрать подходящий":
            func.best_price.best_deal(message, destination_id, count_print, photo_fl)
    else:
        return 0


def get_city(message):
    city = bot.send_message(message.chat.id, "В каком городе будем искать отель?")
    bot.register_next_step_handler(city, func.start.get_id)
