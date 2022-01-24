import tinvest
import math
from decimal import Decimal

from secrets import TOKEN, CONFIG_PATH
from extractor import Extractor
from allocator import Allocator
from funcs import get_config, get_approximated_values


# get config
config = get_config(CONFIG_PATH)

# get client instance
client = tinvest.SyncClient(TOKEN)

extractor_instance = Extractor(
    client_instance=client,
    config=config['extractor'])

extractor_instance.run()

allocator_instance = Allocator(
    data=[extractor_instance.web_data, extractor_instance.portfolio_data],
    balances=[extractor_instance.usd_balance, extractor_instance.total_balance],
    config=config['allocator'])

df = allocator_instance.run()

df.sort_values('required_weight', inplace=True, ascending=False)

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


def printer(stocks):
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

        print(f"-{' ' * stock_left}{stock}{' ' * stock_right}-{' ' * amount_left}{amount}{' ' * amount_right}-", end='\n')
        print('* - * - * - * - * - * -  *')


printer(stocks)

