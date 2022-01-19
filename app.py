import json
import requests
import tinvest
from collections import defaultdict
import pandas as pd
from secrets import TOKEN

import stats_load

# preparation
INDEX_NAME = 'nasdaq100'
stats = stats_load.url_parse(INDEX_NAME)
portfolio_df = stats_load.stats_load(stats)


# get tickers info {ticker: weight}
tickers_info = defaultdict()
for elem in portfolio_df.itertuples():
    ticker = elem[3]
    weight = elem[4]

    tickers_info[ticker] = weight


# get list of tickers
TICKERS = list()
for k in tickers_info.keys():
    TICKERS.append(k)


# get client instance
client = tinvest.SyncClient(TOKEN)

# get portfolio and currencies balance
portfolio = client.get_portfolio()
currencies = client.get_portfolio_currencies()


# currencies parser
CURRENCY = 'usd'
CURRENCY_BALANCE = 0
for currency in currencies.payload.currencies:
    name = currency.currency.name
    balance = currency.balance

    CURRENCY_BALANCE += balance if name.lower() in CURRENCY else 0


# get assets from portfolio that consists in index
my_columns = ['asset', 'amount', 'price', 'weight', 'asset_investments']
df = pd.DataFrame(columns=my_columns)

for position in portfolio.payload.positions:
    ticker = position.ticker

    if ticker not in 'USD000UTSTOM' and ticker in TICKERS:
        amount = position.lots
        price = position.average_position_price.value

        asset_investments = price * amount

        df = df.append(pd.DataFrame([[ticker,
                                      amount,
                                      price,
                                      0,
                                      asset_investments]],
                                    columns=my_columns))

# get total investments
TOTAL_INVESTMENTS = sum(df['asset_investments']) + CURRENCY_BALANCE

# weight calculation
for elem in df.itertuples():
    ticker = elem[1]
    asset_investments = elem[5]
    weight = asset_investments / TOTAL_INVESTMENTS
    df.loc[df['asset'] == ticker, 'weight'] = weight

