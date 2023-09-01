from telebot import types
from _site_api.functions import *
from _sql_bd_api.bd_function import *
from _bot_api import bot, markup_base, help_str


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Приветствую, я бот для поиска подходящих отелей.')
    bot.send_message(message.chat.id, 'Введите /help для просмотра всех команд')
    get_city(message)


@bot.message_handler(commands=['history'])
def history(message):
    usr_history = get_history(message.chat.id)

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

    get_city(message)


@bot.message_handler(commands=['historydelete'])
def history_delete(message):
    delete_history(message.chat.id)
    bot.send_message(message.chat.id, "История запросов успешно удалена\n")
    get_city(message)


@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.send_message(message.chat.id, 'Бот для поиска подходящих отелей\nСписок команд:\n\n' + help_str)
    get_city(message)


@bot.message_handler(commands=['lowprice'])
def low(message, destination_id, count_print, photo_fl):
    if check_command(message):
        return 1
    if destination_id == 0 or count_print == 0:
        get_city(message)

    response = site_low_req(destination_id, count_print)

    for item in json.loads(response.text)["data"]["propertySearch"]["properties"]:
        name     = item["name"]
        score    = item["reviews"]["score"]
        total    = item["reviews"]["total"]
        price    = item["price"]["lead"]["formatted"]
        stars    = item["star"]
        distance = item["destinationInfo"]["distanceFromDestination"]["value"]

        add_history(message.chat.id, name, score, total, price, stars, distance)

        bot.send_message(message.chat.id,
                         "{}\nОтзывы {}/10 ({})\nЦена за ночь:{}\n{}🌟\nРасстояние до центра: {}\n".format(
                             name,
                             score,
                             total,
                             price,
                             stars,
                             distance
                         ), reply_markup=markup_base)
        if photo_fl:
            try:
                bot.send_photo(message.chat.id, item["propertyImage"]["image"]["url"])
            except ValueError:
                bot.send_message(message.chat.id, "Фотографий нет", reply_markup=markup_base)


@bot.message_handler(commands=['bestdeal'])
def best_deal(message, destination_id, count_print, photo_fl=False):
    if check_command(message):
        return 1
    if destination_id == 0 or count_print == 0:
        get_city(message)
        return

    min_cost_m = bot.send_message(message.chat.id, "Введите минимальную цену", reply_markup=markup_base)
    bot.register_next_step_handler(min_cost_m, get_min_cost, destination_id, count_print, photo_fl)


def get_min_cost(message, destination_id, count_print, photo_fl):
    if check_command(message):
        return 1
    min_cost = message.text
    max_cost_m = bot.send_message(message.chat.id, "Введите максимальную цену", reply_markup=markup_base)
    bot.register_next_step_handler(max_cost_m, get_max_cost, destination_id, count_print, photo_fl, min_cost)


def get_max_cost(message, destination_id, count_print, photo_fl, min_cost, max_cost=0):
    if check_command(message):
        return 1
    if max_cost == 0:
        max_cost = message.text

    try:
        if int(min_cost) > int(max_cost):
            bot.send_message(message.chat.id, "Попробуйте еще раз", reply_markup=markup_base)
            best_deal(message, destination_id, count_print, photo_fl)
            return

    except ValueError:
        bot.send_message(message.chat.id, "Попробуйте ещё раз", reply_markup=markup_base)
        best_deal(message, destination_id, count_print, photo_fl)

    min_star = bot.send_message(message.chat.id, "Введите минимальное количество звезд", reply_markup=markup_base)
    bot.register_next_step_handler(min_star, get_min_star, destination_id, count_print, photo_fl, min_cost, max_cost)


def get_min_star(message, destination_id, count_print, photo_fl, min_cost, max_cost):
    if check_command(message):
        return 1
    min_star = message.text

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
        err_star = bot.send_message(message.chat.id, "Нужно целое число от 1 до 5", reply_markup=markup_base)
        get_max_cost(err_star, destination_id, count_print, photo_fl, min_cost, max_cost)
        return

    send_best(message, destination_id, count_print, photo_fl, min_cost, max_cost, stars_count)


def send_best(message, destination_id, count_print, photo_fl, min_cost, max_cost, stars_count):
    if check_command(message):
        return 1
    response = site_best_req(destination_id, count_print, min_cost, max_cost, stars_count)

    for item in json.loads(response.text)["data"]["propertySearch"]["properties"]:

        name = item["name"]
        score = item["reviews"]["score"]
        total = item["reviews"]["total"]
        price = item["price"]["lead"]["formatted"]
        stars = item["star"]
        distance = item["destinationInfo"]["distanceFromDestination"]["value"]

        add_history(message.chat.id, name, score, total, price, stars, distance)

        bot.send_message(message.chat.id,
                         "{}\nОтзывы {}/10 ({})\nЦена за ночь:{}\n{}🌟\nРасстояние до центра: {}\n".format(
                             name,
                             score,
                             total,
                             price,
                             stars,
                             distance
                         ), reply_markup=markup_base)

        if photo_fl:
            try:
                bot.send_photo(message.chat.id, item["propertyImage"]["image"]["url"])
            except ValueError:
                bot.send_message(message.chat.id, "Фотографий нет", reply_markup=markup_base)


@bot.message_handler(func=lambda x: False)
def menu_button(message, destination_id, count_print):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_low = types.KeyboardButton("Топ дешевых")
    item_choice = types.KeyboardButton("Подобрать подходящий")
    item_back = types.KeyboardButton("Вернуться в начало")

    markup.add(item_low, item_choice, item_back)

    if message.text == "Да":
        photo_flag = True
    else:
        photo_flag = False

    choice = bot.send_message(message.chat.id, "Отлично, теперь выберите из вариантов ниже:", reply_markup=markup)
    bot.register_next_step_handler(choice, check_command, destination_id, count_print, photo_flag)


def get_city(message):
    city = bot.send_message(message.chat.id, "В каком городе будем искать отель?")
    bot.register_next_step_handler(city, get_id)


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
    markup_bool = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_yes = types.KeyboardButton("Да")
    item_no = types.KeyboardButton("Нет")

    markup_bool.add(item_yes, item_no)

    photo = bot.send_message(message.chat.id, "Отображать фотографии?", reply_markup=markup_bool)
    bot.register_next_step_handler(photo, menu_button, destination_id, count_print)


@bot.message_handler(content_types=["text"])
def check_command(message, destination_id=0, count_print=0, photo_fl=False):
    if message.text in ("Вернуться в начало", "/back", "/start"):
        send_welcome(message)
        return 1
    elif message.text in ("Список команд", "/help"):
        help_bot(message)
        return 1
    elif message.text == "/history":
        history(message)
        return 1
    elif message.text == "/historydelete":
        history_delete(message)
        return 1
    elif destination_id and count_print:
        if message.text == 'Топ дешевых':
            low(message, destination_id, count_print, photo_fl)
        elif message.text == "Подобрать подходящий":
            best_deal(message, destination_id, count_print, photo_fl)
    else:
        return 0
