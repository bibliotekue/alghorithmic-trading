from funcs import get_config
import pandas as pd
from secrets import CONFIG_PATH
from decimal import Decimal


class Allocator:

    def __init__(self, data, balances, config_path):
        self.config = get_config(config_path)['allocator']

        self.web_data, self.portfolio_data = data
        self.usd_balance, self.total_balance = balances

    def parse_elem(self, elem):
        symbol = elem[3]
        official_weight = Decimal(elem[4] / 100)
        official_price = elem[5]

        return symbol, official_weight, official_price

    def check_allocation(self, symbol):
        try:
            total_asset_sum = self.portfolio_data.query(f"asset == '{symbol}'")['asset_investments'][0]
            weight = self.portfolio_data.query(f"asset == '{symbol}'")['weight'][0]
        except Exception:
            total_asset_sum = 0
            weight = 0

        return total_asset_sum, weight

    def calculating_requirements(self, weight, official_weight, official_price, total_asset_sum):
        required_weight = official_weight - weight
        if required_weight > 0:
            required_allocation = self.total_balance * required_weight
            required_investments = required_allocation - total_asset_sum
            if required_investments > 0:
                required_amount = required_investments / Decimal(official_price)
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

            # adding recommendation
            df = df.append(pd.DataFrame([[
                symbol,
                required_investments,
                required_weight,
                required_amount,
                official_price]],
                columns=self.config['columns_for_recommendation']))

            self.usd_balance -= required_investments

        return df