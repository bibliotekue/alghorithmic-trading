import json
import os
from decimal import Decimal
import math


INDEXES = {
    'sp500': 'sp500',
    'nasdaq': 'nasdaq100',
    'dowjones': 'dowjones'
}


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

        if math.ceil(amount) and usd_balance >= price * math.ceil(amount):
            stocks.append((ticker, math.ceil(amount)))
            usd_balance -= (price * amount)

        elif math.floor(amount) > 0 and usd_balance >= price * math.floor(amount):
            stocks.append((ticker, math.floor(amount)))
            usd_balance -= (price * amount)

    return stocks


def get_printed(stocks):
    shift = 13

    print(f'''
* - * - * - * - * - * -  *
-   stock   -   amount   -
* - * - * - * - * - * -  *''', end='\n')

    for stock, amount in stocks:
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