import json

from _site_api.lower_request import site_low_req
from _sql_bd_api.bd_add_history import add_history

from .check import *


@bot.message_handler(commands=["lowprice"])
def low(message, destination_id, count_print, photo_fl):
    if check_command(message):
        return 1
    if destination_id == 0 or count_print == 0:
        get_city(message)

    response = site_low_req(destination_id, count_print)

    for item in json.loads(response.text)["data"]["propertySearch"]["properties"]:
        name = item["name"]
        score = item["reviews"]["score"]
        total = item["reviews"]["total"]
        price = item["price"]["lead"]["formatted"]
        stars = item["star"]
        distance = item["destinationInfo"]["distanceFromDestination"]["value"]

        add_history(message.chat.id, name, score, total, price, stars, distance)

        bot.send_message(
            message.chat.id,
            "{}\nОтзывы {}/10 ({})\nЦена за ночь:{}\n{}🌟\nРасстояние до центра: {}\n".format(
                name, score, total, price, stars, distance
            ),
            reply_markup=markup_base,
        )
        if photo_fl:
            try:
                bot.send_photo(message.chat.id, item["propertyImage"]["image"]["url"])
            except ValueError:
                bot.send_message(
                    message.chat.id, "Фотографий нет", reply_markup=markup_base
                )
