import json
import os
import math
from collections import defaultdict

import pandas as pd
from decimal import Decimal


def get_config(absolute_path: str) -> dict:
    '''
    Read config from json file and loads it to a python dictionary object.

    :param absolute_path: your absolute path to config which already exists in project root.
    :return: config file as a python dictionary.
    '''

    if os.path.isfile(absolute_path):
        with open(absolute_path) as file:
            config = json.loads(file.read())
    return config


def get_approximated_amount(df: pd.DataFrame, usd_balance: Decimal) -> defaultdict:
    '''
    Calculate approximate amount of stocks to buy based on recommended allocations.

    :param df: pandas DataFrame with recommended allocations.
    :param usd_balance: dollar balance of your Tinkoff.Invest portfolio.
    :return: a dict with ticker as a key and amount of stocks to buy as a value.
    '''
    stocks = defaultdict()

    for i in df.values:
        ticker = i[0]
        amount = i[3]
        price = Decimal(i[4])

        if math.ceil(amount) and usd_balance >= price * math.ceil(amount):
            stocks[ticker] = math.ceil(amount)
            usd_balance -= (price * amount)

        elif math.floor(amount) and usd_balance >= price * math.floor(amount):
            stocks[ticker] = math.floor(amount)
            usd_balance -= (price * amount)

    return stocks


def get_printed(stocks: defaultdict) -> None:
    '''
    Outputs the needed allocation for mirroring the chosen Index to the console in a pretty format.

    :param stocks: dict with ticker as a key and amount of stocks to buy as a value.
    :return: None, just printing pretty result to console.
    '''
    shift = 13

    print(f'''
* - * - * - * - * - * -  *
-   stock   -   amount   -
* - * - * - * - * - * -  *''', end='\n')

    for stock, amount in stocks.items():
        stock_length = len(stock)
        stock_sides = shift - stock_length
        stock_left = stock_sides // 2 - 1
        stock_right = stock_sides - stock_left - 2

        if amount >= 10:
            amount_sides = 13 - 2
        else:
            amount_sides = 13 - 1

        amount_left = amount_sides // 2 - 1
        amount_right = amount_sides - amount_left - 1

        print(f"-{' ' * stock_left}{stock}{' ' * stock_right}-{' ' * amount_left}{amount}{' ' * amount_right}-",
              end='\n')
        print('* - * - * - * - * - * -  *')
