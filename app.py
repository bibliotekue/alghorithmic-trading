import json
import requests
import tinvest
from secrets import TOKEN

CURRENCY = 'usd'


# def get_portfolio():
#     headers = {'Authorization': 'Bearer %s' % TOKEN}
#     api = 'https://api-invest.tinkoff.ru/openapi/'
#     endpoint = 'portfolio'
#     response = requests.get(api + endpoint, headers=headers).json()
#     return response


client = tinvest.SyncClient(TOKEN)

portfolio = client.get_portfolio()
currencies = client.get_portfolio_currencies()

total_investments = 0

for currency in currencies.payload.currencies:
    name = currency.currency.name
    balance = currency.balance
    total_investments += balance if name.lower() in CURRENCY else 0
    print(name, balance)

print('\n')

for position in portfolio.payload.positions:
    ticker = position.ticker
    amount = position.lots
    price = position.average_position_price.value
    currency = position.average_position_price.currency

    investments = price * amount
    total_investments += investments if currency.lower() in CURRENCY else 0
    print(ticker, amount, price)

print(total_investments)