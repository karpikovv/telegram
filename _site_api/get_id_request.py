import requests
from config_data.config import headers
import json


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
