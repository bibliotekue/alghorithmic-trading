from bs4 import BeautifulSoup
import requests
import pandas as pd

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

        self.web_data = None
        self.portfolio_data = None

        self.usd_balance = 0  # your usd balance in Tinkoff.Invest
        self.investments_balance = 0  # amount of money in financial instruments
        self.total_balance = 0  # sum of your usd balance and investments

    def extract_web_data(self, url_info: dict) -> None:
        '''
        Extracting data about chosen Index from web-site which includes these fields:
        "#", "Company", "Symbol", "Weight", "Price" and save it to DataFrame.

        :param url_info: python dictionary with info about the web-site defined in config file.
        :return: None
        '''

        response = requests.get(url_info['url'] + url_info['index'], headers=url_info['header'])
        soup = BeautifulSoup(response.text, url_info['parser'])
        index_info = soup.find(url_info['tag'], class_=url_info['attrs'])

        self.web_data = pd.read_html(str(index_info))[0]
        self.web_data = self.web_data[url_info['columns_for_web_data']]

    def extract_portfolio_data(self, portfolio_info: dict) -> None:
        '''
        Extracting data about chosen Index from Tinkoff.Invest which includes these fields:
        "Asset", "Amount", "Price", "Weight", "Asset_investments" and save it to DataFrame.

        :param portfolio_info: python dictionary with info about your portfolio defined in config file.
        :return: None
        '''
        self.portfolio_data = pd.DataFrame(columns=portfolio_info['columns_for_portfolio_data'])
        tickers = self.web_data['Symbol'].values

        for position in self.portfolio_instance.payload.positions:
            ticker = position.ticker

            if ticker not in 'USD000UTSTOM' and ticker in tickers:
                amount = position.lots
                price = position.average_position_price.value

                asset_investments = price * amount

                self.portfolio_data = self.portfolio_data.append(pd.DataFrame([[
                                                                ticker,
                                                                amount,
                                                                price,
                                                                0,
                                                                asset_investments]],
                                            columns=portfolio_info['columns_for_portfolio_data']))

    def get_portfolio_balances(self) -> None:
        '''
        Extracting data about your Tinkoff.Invest balances such as:
        "Usd balance", "Investments balance", "Total balance" by using "tinvest" methods.

        :return: None
        '''
        self.usd_balance = self.currencies_instance.payload.currencies[2].balance
        self.investments_balance = sum(self.portfolio_data['asset_investments'])

        self.total_balance = self.usd_balance + self.investments_balance

    def calculate_assets_weights(self) -> None:
        '''
        Calculates assets weights in your Tinkoff.Invest portfolio by looping "portfolio_data" and write it in "weight"
        column in portfolio DataFrame.

        :return: None
        '''
        for elem in self.portfolio_data.itertuples():
            ticker = elem[1]
            asset_investments = elem[5]
            weight = asset_investments / self.total_balance
            self.portfolio_data.loc[self.portfolio_data['asset'] == ticker, 'weight'] = weight

    def run(self) -> None:
        self.extract_web_data(self.config['url_info'])
        self.extract_portfolio_data(self.config['portfolio_info'])
        self.get_portfolio_balances()
        self.calculate_assets_weights()
