import json
import requests
import tinvest
import pandas as pd
from secrets import TOKEN

import webscrapper
import analyzer


# get client instance
client = tinvest.SyncClient(TOKEN)

# get portfolio and currencies balance
portfolio = client.get_portfolio()
currencies = client.get_portfolio_currencies()

web_data = webscrapper.extract_web_data(index=webscrapper.INDEXES['NASDAQ'])
portfolio_data = analyzer.extract_portfolio_data(portfolio, web_data['Symbol'].values)

# get balances
usd_balance = currencies.payload.currencies[2].balance
total_investments = sum(portfolio_data['asset_investments'])

total_balance = total_investments + usd_balance

# weight calculation
for elem in portfolio_data.itertuples():
    ticker = elem[1]
    asset_investments = elem[5]
    weight = asset_investments / total_balance
    portfolio_data.loc[portfolio_data['asset'] == ticker, 'weight'] = weight

print(portfolio_data)

