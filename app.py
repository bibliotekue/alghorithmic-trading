import tinvest

from secrets import TOKEN, CONFIG_PATH
from extractor import Extractor

# get client instance
client = tinvest.SyncClient(TOKEN)

surfer = Extractor(client_instance=client,
                   config_path=CONFIG_PATH)
surfer.run()

print(surfer.portfolio_data)

