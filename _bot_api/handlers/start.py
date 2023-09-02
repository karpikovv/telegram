from .check import *
from _site_api.get_id_request import site_get_id
from ..keyboards.reply_bool import markup_bool


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Приветствую, я бот для поиска подходящих отелей.')
    bot.send_message(message.chat.id, 'Введите /help для просмотра всех команд')
    get_city(message)


def get_id(message):
    if check_command(message):
        return 1
    destination_id, name = site_get_id(message.text)
    if destination_id:
        bot.send_message(message.chat.id, "Поиск: \n{}".format(name), reply_markup=markup_base)
        count_message = bot.send_message(message.chat.id, "Сколько отелей отобразить? (до 24)")
        bot.register_next_step_handler(count_message, get_count, destination_id)
    else:
        bot.send_message(message.chat.id,
                         'К сожалению, данных о {} пока нет.\nУбедитесь что название города написано на латинице и '
                         'попробуйте еще раз'.format(message.text), reply_markup=markup_base)
        get_city(message)


def get_count(message, destination_id):
    if check_command(message):
        return 1
    if message.text.isdigit() and (0 < int(message.text) < 26):
        count_print = int(message.text)
        get_photo(message, destination_id, count_print)
    else:
        count = bot.send_message(message.chat.id, "Сколько отелей отобразить? (до 24)", reply_markup=markup_base)
        bot.register_next_step_handler(count, get_count, destination_id)


@bot.message_handler(func=lambda x: False)
def get_photo(message, destination_id, count_print):

    photo = bot.send_message(message.chat.id, "Отображать фотографии?", reply_markup=markup_bool)
    bot.register_next_step_handler(photo, func.menu.menu_button, destination_id, count_print)
print(5)
