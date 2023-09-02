import json
from _site_api.best_request import site_best_req
from _sql_bd_api.bd_add_history import add_history
from .check import *


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
