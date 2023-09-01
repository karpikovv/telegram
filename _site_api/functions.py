import requests
import json
from _site_api.param import headers


def site_low_req(destination_id, count_print):

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "destination": {"regionId": str(destination_id)},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2025
        },
        "checkOutDate": {
            "day": 11,
            "month": 10,
            "year": 2025
        },
        "rooms": [{"adults": 1}],
        "resultsSize": count_print,
        "sort": "PRICE_LOW_TO_HIGH",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response


def site_best_req(destination_id, count_print, min_cost, max_cost, stars_count):
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "destination": {"regionId": str(destination_id)},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2025
        },
        "checkOutDate": {
            "day": 11,
            "month": 10,
            "year": 2025
        },
        "rooms": [{"adults": 1}],
        "resultsSize": count_print,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {
            "price": {
                "max": int(max_cost),
                "min": int(min_cost)
            },
            "star": stars_count
        }

    }

    response = requests.request("POST", url, json=payload, headers=headers)
    return response


def site_get_id(city):

    querystring_location = {"q": city}
    url_location = "https://hotels4.p.rapidapi.com/locations/v3/search"
    response_location = requests.request("GET", url_location, headers=headers, params=querystring_location)
    hot_text = json.loads(response_location.text)

    if hot_text["sr"][0]["type"] == "CITY":
        name = hot_text["sr"][0]["regionNames"]["fullName"]
        gid = hot_text["sr"][0]["gaiaId"]
        return gid, name
    else:
        return 0, 0
