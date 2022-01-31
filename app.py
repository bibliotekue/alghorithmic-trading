import tinvest

from utils.secrets import TOKEN, CONFIG_PATH

from src.consoller import args
from src.extractor import Extractor
from src.allocator import Allocator
from src.funcs import get_config, get_approximated_amount, get_printed


INDEXES = {
    'sp500': 'sp500',
    'nasdaq': 'nasdaq100',
    'dowjones': 'dowjones'
}

INDEX_ARG = args.index

# get config
config = get_config(CONFIG_PATH)

# get client instance
client = tinvest.SyncClient(TOKEN)

# argparser
if INDEX_ARG.lower() in INDEXES.keys():
    config['extractor']['url_info']['index'] = INDEXES[INDEX_ARG.lower()]
    print(config['extractor']['url_info']['index'])

# get extractor instance
extractor_instance = Extractor(
    client_instance=client,
    config=config['extractor'])

data, balances = extractor_instance.run()

# get allocator instance
allocator_instance = Allocator(
    data=data,
    balances=balances,
    config=config['allocator'])

df = allocator_instance.run()

df.sort_values('required_weight', inplace=True, ascending=False)

# approximating
stocks = get_approximated_amount(df=df, usd_balance=balances[0])

# printing allocation
get_printed(stocks)

