import random

import requests

from Utils.logger import logger
from constants import user_agents


def get_product_UPC_data(upc_code):
    user_agent = random.choice(user_agents)
    base_url = "https://api.upcitemdb.com/prod/trial/lookup"
    headers = {"Content-Type": "application/json","User-Agent": user_agent}
    params = {"q": upc_code}
    weight = None
    images = None
    try:
        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()
        print(data)

        # Extracting weight information
        if data["items"]:
            try:
                images = data["items"][0].get("images")
            except Exception:
                images = None
            try:
                weight = data["items"][0].get("weight")
            except Exception:
                weight = None
    except requests.exceptions.RequestException as e:
        logger.error("Error has occured while retrieving data from UPCemdb")

    finally:
        return weight, images

print(get_product_UPC_data("LG 43” Class UQ75 Series LED 4K UHD Smart webOS TV"))