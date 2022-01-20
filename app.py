import tinvest

from secrets import TOKEN, CONFIG_PATH
from extractor import Extractor
from allocator import Allocator

# get client instance
client = tinvest.SyncClient(TOKEN)

surfer = Extractor(client_instance=client,
                   config_path=CONFIG_PATH)

surfer.run()

recommender = Allocator(data=[surfer.web_data, surfer.portfolio_data],
                        balances=[surfer.usd_balance, surfer.total_balance],
                        config_path=CONFIG_PATH)

df = recommender.run()

df.sort_values('required_amount', inplace=True, ascending=False)

df.to_csv('rec.csv')
