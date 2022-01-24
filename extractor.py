from bs4 import BeautifulSoup
import requests
import pandas as pd
import funcs


class Extractor:

    def __init__(self, client_instance, config):
        self.config = config

        self.portfolio_instance = client_instance.get_portfolio()
        self.currencies_instance = client_instance.get_portfolio_currencies()

        self.web_data = None
        self.portfolio_data = None

        self.usd_balance = 0
        self.investments_balance = 0
        self.total_balance = 0

    def extract_web_data(self, url_info):

        response = requests.get(url_info['url'] + url_info['index'], headers=url_info['header'])
        soup = BeautifulSoup(response.text, url_info['parser'])
        index_info = soup.find(url_info['tag'], class_=url_info['attrs'])

        self.web_data = pd.read_html(str(index_info))[0]
        self.web_data = self.web_data[url_info['columns_for_web_data']]

    def extract_portfolio_data(self, portfolio_info):
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

    def get_portfolio_balances(self):
        self.usd_balance = self.currencies_instance.payload.currencies[2].balance
        self.investments_balance = sum(self.portfolio_data['asset_investments'])

        self.total_balance = self.usd_balance + self.investments_balance

    def calculate_assets_weights(self):
        for elem in self.portfolio_data.itertuples():
            ticker = elem[1]
            asset_investments = elem[5]
            weight = asset_investments / self.total_balance
            self.portfolio_data.loc[self.portfolio_data['asset'] == ticker, 'weight'] = weight

    def run(self):
        self.extract_web_data(self.config['url_info'])
        self.extract_portfolio_data(self.config['portfolio_info'])
        self.get_portfolio_balances()
        self.calculate_assets_weights()
