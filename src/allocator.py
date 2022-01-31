import pandas as pd
from decimal import Decimal


class Allocator:
    '''
    This class is calculating requirement allocation for Index mirroring. Firstly, "parse_elem" method is parsing web-data.
    Then, "check_allocation" method is checking your current allocation in your Tinkoff.Invest portfolio for each asset
    which includes in chosen Index. And, finally "calculating_requirements" method calculates a list of stocks based on
    your current balances for mirroring chosen Index.
    '''

    def __init__(self, data: list, balances: list, config: dict) -> None:
        '''

        :param data: a list of web-data and your Tinkoff.Invest portfolio data.
        :param balances: a list of your usd and total balances in Tinkoff.Invest portfolio.
        :param config: config file as a python dictionary which will help to calculate allocation.
        '''
        self.config = config

        self.web_data, self.portfolio_data = data
        self.usd_balance, self.total_balance = balances

    def parse_elem(self, elem: tuple) -> [str, Decimal, Decimal]:
        '''
        This method extracts data from pandas itertuples object such as "Symbol", "Official_weight" and "Official_price"

        :param elem: pandas itertuples object
        :return: extracting data from pandas itertuples object
        '''
        symbol = elem[3]
        official_weight = Decimal(elem[4] / 100)
        official_price = Decimal(elem[5])

        return symbol, official_weight, official_price

    def check_allocation(self, symbol: str) -> (int, int):
        '''
        Checks your current Tinkoff.Invest portfolio allocation based on chosen Index.

        :param symbol: asset ticker name.
        :return: total amount of money which spends on this asset and his weight in your Tinkoff.Invest portfolio.
        '''
        try:
            total_asset_sum = self.portfolio_data.query(f"asset == '{symbol}'")['asset_investments'][0]
            weight = self.portfolio_data.query(f"asset == '{symbol}'")['weight'][0]
        except Exception:
            total_asset_sum = 0
            weight = 0

        return total_asset_sum, weight

    def calculating_requirements(self,
                                 weight: int,
                                 official_weight: Decimal,
                                 official_price: Decimal,
                                 total_asset_sum: int) -> (Decimal, Decimal, Decimal):
        '''
        Calculates requirement allocation for mirroring the chosen Index. It considered current amount
        of financial instruments in your Tinkoff.Invest portfolio therefore requirement asset weight and finally amount
        of stocks to buy.

        :param weight: asset weight in Tinkoff.Invest portfolio.
        :param official_weight: asset weight in chosen Index.
        :param official_price: asset current price.
        :param total_asset_sum: total amount of money which spends on this asset.
        :return: tuple with requirement allocation for mirroring the chosen Index.
        '''
        required_weight = official_weight - weight
        if required_weight > 0:
            required_allocation = self.total_balance * required_weight
            required_investments = required_allocation - total_asset_sum
            if required_investments > 0:
                if int(official_price):
                    required_amount = required_investments / official_price
                    return required_investments, required_weight, required_amount
        return 0, 0, 0

    def run(self):
        df = pd.DataFrame(columns=self.config['columns_for_recommendation'])

        for elem in self.web_data.itertuples():
            # define necessary variables
            symbol, official_weight, official_price = self.parse_elem(elem)
            total_asset_sum, weight = self.check_allocation(symbol)
            required_investments, required_weight, required_amount = self.calculating_requirements(
                                                                                                weight,
                                                                                                official_weight,
                                                                                                official_price,
                                                                                                total_asset_sum)

            # adding recommendation to DataFrame
            df = df.append(pd.DataFrame([[
                symbol,
                required_investments,
                required_weight,
                required_amount,
                official_price]],
                columns=self.config['columns_for_recommendation']))

            self.usd_balance -= required_investments

        return df