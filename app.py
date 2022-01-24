import tinvest

from secrets import TOKEN, CONFIG_PATH

from src.extractor import Extractor
from src.allocator import Allocator
from src.funcs import get_config, get_approximated_values, get_printed


# get config
config = get_config(CONFIG_PATH)

# get client instance
client = tinvest.SyncClient(TOKEN)

# get extractor instance
extractor_instance = Extractor(
    client_instance=client,
    config=config['extractor'])

extractor_instance.run()

# get allocator instance
allocator_instance = Allocator(
    data=[extractor_instance.web_data, extractor_instance.portfolio_data],
    balances=[extractor_instance.usd_balance, extractor_instance.total_balance],
    config=config['allocator'])

df = allocator_instance.run()

df.sort_values('required_weight', inplace=True, ascending=False)

# approximating
stocks = get_approximated_values(df, extractor_instance.usd_balance)

# printing allocation
get_printed(stocks)

