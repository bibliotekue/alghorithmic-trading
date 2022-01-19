import pandas as pd


# get assets info from portfolio that consists in index
MY_COLUMNS = ['asset', 'amount', 'price', 'weight', 'asset_investments']


def extract_portfolio_data(portfolio, index_tickers, columns=MY_COLUMNS):
    df = pd.DataFrame(columns=columns)
    for position in portfolio.payload.positions:
        ticker = position.ticker

        if ticker not in 'USD000UTSTOM' and ticker in index_tickers:  # data['Symbol'].values
            amount = position.lots
            price = position.average_position_price.value

            asset_investments = price * amount

            df = df.append(pd.DataFrame([[ticker,
                                          amount,
                                          price,
                                          0,
                                          asset_investments]],
                                        columns=MY_COLUMNS))

    return df
