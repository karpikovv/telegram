import requests
from config_data.config import headers


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
