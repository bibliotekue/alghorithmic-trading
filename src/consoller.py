import argparse

parser = argparse.ArgumentParser(description='This program is analysis your Tinkoff.Invest portfolio and returned '
                                             'a list of stocks and their amount to mirror chosen Index. ')

parser.add_argument('-i',
                    "--index",
                    help="Index which you want to mirror. There is only 3 indexes such as: SP500, NASDAQ and DOWJONES.",
                    default='SP500')

args = parser.parse_args()
