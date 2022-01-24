import json
import os
from decimal import Decimal
import math


def get_config(absolute_path):
    if os.path.isfile(absolute_path):
        with open(absolute_path) as file:
            config = json.loads(file.read())
    return config


def get_approximated_values(df, usd_balance):
    stocks = list()

    for i in df.values:
        ticker = i[0]
        amount = i[3]
        price = Decimal(i[4])

        if math.ceil(amount) and extractor_instance.usd_balance >= price * math.ceil(amount):
            stocks.append((ticker, math.ceil(amount)))
            extractor_instance.usd_balance -= (price * amount)

        elif math.floor(amount) > 0 and extractor_instance.usd_balance >= price * math.floor(amount):
            stocks.append((ticker, math.floor(amount)))
            extractor_instance.usd_balance -= (price * amount)

        else:
            pass