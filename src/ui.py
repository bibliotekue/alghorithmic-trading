import os
import sys
import inspect
import argparse
from funcs import get_config, INDEXES

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from secrets import CONFIG_PATH


parser = argparse.ArgumentParser(description='This program is analysis your Tinkoff.Invest portfolio and returned '
                                             'a list of stocks and their amount to mirror chosen Index. ')

parser.add_argument("-s",
                    "--save",
                    help="Save a list of stocks and their amount to .csv.",
                    action='store_true')

parser.add_argument('-i',
                    "--index",
                    help="Index which you want to mirror. There is only 3 indexes such as: SP500, NASDAQ and DOWJONES.",
                    default='SP500')

args = parser.parse_args()

if args.save:
    print('saving to .csv')
    pass

if args.index.lower() in INDEXES.keys():
    config = get_config(CONFIG_PATH)['extractor']
    config['index'] = INDEXES[args.index.lower()]



