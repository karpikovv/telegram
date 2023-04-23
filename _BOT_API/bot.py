from telebot import types
from _SITE_API.functions import *
from _BOT_API import bot

help_str = '/lowprice - Узнать топ самых дешёвых отелей в городе\n\n' \
           '/highprice - Узнать топ самых дорогих отелей в городе\n\n' \
           '/bestdeal - Узнать топ отелей, наиболее подходящих по цене и расположению от центра\n\n' \
           '/history - Узнать историю поиска отелей\n\n'


@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.send_message(message.chat.id, 'Приветствую, я бот для поиска подходящих отелей.')
    get_city(message)


def get_city(message):

    city = bot.send_message(message.chat.id, "Где будем искать?")
    bot.register_next_step_handler(city, get_id)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Бот для поиска подходящих отелей\nСписок команд:\n\n' + help_str)


@bot.message_handler(commands=['lowprice'])
def low(message, destination_id, count_print):

    if destination_id == 0 or count_print == 0:
        print(2)
        get_city(message)

    response = site_low_req(destination_id, count_print)

    for item in json.loads(response.text)["data"]["propertySearch"]["properties"]:
        bot.send_message(message.chat.id,
            "{}\nОтзывы {}/10 ({})\nЦена за ночь:{}\n{}🌟\nРасстояние до центра: {}\n".format(
                 item["name"],
                 item["reviews"]["score"],
                 item["reviews"]["total"],
                 item["price"]["lead"]["formatted"],
                 item["star"],
                 item["destinationInfo"]["distanceFromDestination"]["value"]
            ))


def get_min_cost(message, destination_id, count_print):
    min_cost = message.text
    max_cost_m = bot.send_message(message.chat.id, "Введите максимальную цену\n(местная валюта)")
    bot.register_next_step_handler(max_cost_m, get_max_cost, destination_id, count_print, min_cost)


def get_max_cost(message, destination_id, count_print, min_cost, max_cost=0):

    if max_cost == 0:
        max_cost = message.text

    try:
        if int(min_cost) > int(max_cost):
            bot.send_message(message.chat.id, "Попробуйте еще раз")
            best_deal(message, destination_id, count_print)
            return

    except ValueError:
        bot.send_message(message.chat.id, "Попробуйте ещё раз")
        best_deal(message, destination_id, count_print)

    min_star = bot.send_message(message.chat.id, "Введите минимальное количество звезд")
    bot.register_next_step_handler(min_star, get_min_star, destination_id, count_print, min_cost, max_cost)


def get_min_star(message, destination_id, count_print, min_cost, max_cost):
    min_star = message.text
    stars_count = []

    if min_star == "1":
        stars_count = ["10", "20", "30", "40", "50"]
    elif min_star == "2":
        stars_count = ["20", "30", "40", "50"]
    elif min_star == "3":
        stars_count = ["30", "40", "50"]
    elif min_star == "4":
        stars_count = ["40", "50"]
    elif min_star == "5":
        stars_count = ["50"]
    else:
        err_star = bot.send_message(message.chat.id, "Нужно целое число от 1 до 5")
        get_max_cost(err_star, destination_id, count_print, min_cost, max_cost)
        return

    send_best(message, destination_id, count_print, min_cost, max_cost, stars_count)


def send_best(message, destination_id, count_print, min_cost, max_cost, stars_count):

    response = site_best_req(destination_id, count_print, min_cost, max_cost, stars_count)

    for item in json.loads(response.text)["data"]["propertySearch"]["properties"]:
        bot.send_message(message.chat.id,
             "{}\nОтзывы {}/10 ({})\nЦена за ночь:{}\n{}🌟\nРасстояние до центра: {}\n".format(
                 item["name"],
                 item["reviews"]["score"],
                 item["reviews"]["total"],
                 item["price"]["lead"]["formatted"],
                 item["star"],
                 item["destinationInfo"]["distanceFromDestination"]["value"]
             ))


@bot.message_handler(commands=['bestdeal'])
def best_deal(message, destination_id, count_print):

    if destination_id == 0 or count_print == 0:
        get_city(message)
        return

    min_cost_m = bot.send_message(message.chat.id, "Введите минимальную цену\n(местная валюта)")
    bot.register_next_step_handler(min_cost_m, get_min_cost, destination_id, count_print)


@bot.message_handler(commands=['history'])
def history(message):
    bot.reply_to(message, "Func history")


@bot.message_handler(func=lambda x: False)
def menu_button(message, destination_id, count_print):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_low = types.KeyboardButton("Топ дешевых")
    item_choice = types.KeyboardButton("Подобрать подходящий")

    markup.add(item_low, item_choice)
    choice = bot.send_message(message.chat.id, "Отлично, теперь выберите из вариантов ниже:", reply_markup=markup)
    bot.register_next_step_handler(choice, ans_all, destination_id, count_print)


def get_id(message):

    destination_id, name = site_get_id(message.text)
    if destination_id:
        bot.send_message(message.chat.id, "Поиск: \n{}".format(name))
        count_message = bot.send_message(message.chat.id, "Сколько отелей отобразить? (до 24)")
        bot.register_next_step_handler(count_message, get_count, destination_id)
    else:
        bot.send_message(message.chat.id,
            'К сожалению, данных о {} пока нет.\nУбедитесь что название города написано на латинице и попробуйте еще раз'.format(
                message.text))
        get_city(message)


def get_count(message, destination_id):
    if message.text.isdigit() and (0 < int(message.text) < 26):
        count_print = int(message.text)
        menu_button(message, destination_id, count_print)
    else:
        count = bot.send_message(message.chat.id, "Сколько отелей отобразить? (до 25)")
        bot.register_next_step_handler(count, get_count, destination_id)


@bot.message_handler(content_types=["text"])
def ans_all(message, destination_id=0, count_print=0):
    if message.text == 'Топ дешевых':
        print(1)
        low(message, destination_id, count_print)
    elif message.text == "Подобрать подходящий":
        best_deal(message, destination_id, count_print)
    else:
        bot.send_message(message.chat.id, 'Неизвестная команда, список команд - /help')
