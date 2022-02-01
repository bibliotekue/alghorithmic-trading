from bs4 import BeautifulSoup
import requests
import pandas as pd
from decimal import Decimal

import tinvest


class Extractor:
    '''
    This class is extracting data from web-site (slickcharts.com) and your Tinkoff.Invest portfolio by using
    extract_web_data and extract_portfolio_data methods. Save it to web_data and portfolio_data variables.
    Get your portfolio balances in get_portfolio_balances method and calculates your assets portfolio weights
    which will help us later calculate allocation in the Allocator class.
    '''

    def __init__(self, client_instance: tinvest.clients.SyncClient, config: dict) -> None:
        '''
        :param client_instance: represents your Tinkoff.Invest profile.
        :param config: config file as a python dictionary for extracting data from needed web-site.
        :return: None
        '''
        self.config = config

        self.portfolio_instance = client_instance.get_portfolio()
        self.currencies_instance = client_instance.get_portfolio_currencies()

        self.usd_balance = 0  # your usd balance in Tinkoff.Invest
        self.investments_balance = 0  # amount of money in financial instruments
        self.total_balance = 0  # sum of your usd balance and investments

    @staticmethod
    def extract_web_data(url_info: dict) -> pd.DataFrame:
        '''
        Extracting data about chosen Index from web-site which includes these fields:
        "#", "Company", "Symbol", "Weight", "Price" and save it to DataFrame.

        :param url_info: python dictionary with info about the web-site defined in config file.
        :return: None
        '''

        response = requests.get(url_info['url'] + url_info['index'], headers=url_info['header'])
        soup = BeautifulSoup(response.text, url_info['parser'])
        index_info = soup.find(url_info['tag'], class_=url_info['attrs'])

        web_data = pd.read_html(str(index_info))[0]
        web_data = web_data[url_info['columns_for_web_data']]

        return web_data

    def extract_portfolio_data(self, portfolio_info: dict, web_data: pd.DataFrame) -> pd.DataFrame:
        '''
        Extracting data about chosen Index from Tinkoff.Invest which includes these fields:
        "Asset", "Amount", "Price", "Weight", "Asset_investments" and save it to DataFrame.

        :param portfolio_info: python dictionary with info about your portfolio defined in config file.
        :param web_data: an extracting data from web source
        :return: a Dataframe with portfolio information
        '''

        portfolio_data = pd.DataFrame(columns=portfolio_info['columns_for_portfolio_data'])
        tickers = web_data['Symbol'].values

        for position in self.portfolio_instance.payload.positions:
            ticker = position.ticker

            if ticker not in 'USD000UTSTOM' and ticker in tickers:
                amount = position.lots
                price = position.average_position_price.value

                asset_investments = price * amount

                portfolio_data = portfolio_data.append(pd.DataFrame([[
                                                                ticker,
                                                                amount,
                                                                price,
                                                                0,
                                                                asset_investments]],
                                            columns=portfolio_info['columns_for_portfolio_data']))

        return portfolio_data

    def get_portfolio_balances(self, portfolio_data: pd.DataFrame) -> tuple[Decimal, int, int]:
        '''
        Extracting data about your Tinkoff.Invest balances such as:
        "Usd balance", "Investments balance", "Total balance" by using "tinvest" methods.

        :param portfolio_data: a Dataframe with portfolio information
        :return: None
        '''
        usd_balance = self.currencies_instance.payload.currencies[2].balance
        investments_balance = sum(portfolio_data['asset_investments'])

        total_balance = usd_balance + investments_balance

        return usd_balance, investments_balance, total_balance

    @staticmethod
    def calculate_assets_weights(portfolio_data: pd.DataFrame, total_balance: int) -> None:
        '''
        Calculates assets weights in your Tinkoff.Invest portfolio by looping "portfolio_data" and write it in "weight"
        column in portfolio DataFrame.

        :param portfolio_data: a Dataframe with portfolio information
        :param total_balance: total balance in the portfolio
        :return: None
        '''
        for elem in portfolio_data.itertuples():
            ticker = elem[1]
            asset_investments = elem[5]
            weight = asset_investments / total_balance
            portfolio_data.loc[portfolio_data['asset'] == ticker, 'weight'] = weight

    def run(self) -> list:
        web_data = self.extract_web_data(self.config['url_info'])

        portfolio_data = self.extract_portfolio_data(self.config['portfolio_info'], web_data)

        usd_balance, investment_balance, total_balance = self.get_portfolio_balances(portfolio_data)

        self.calculate_assets_weights(portfolio_data, total_balance)

        return [[web_data, portfolio_data], [usd_balance, total_balance]]
