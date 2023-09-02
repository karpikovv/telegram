import requests
from config_data.config import headers


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
