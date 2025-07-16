import asyncio
from finviz.finviz import Finviz
from finviz.extract_tickers import *

# Path
only_tickers_path = './csvs/only_tickers/'

# Finviz
fv = Finviz()

# Stocks News Tickers
async def news():
    n = await fv.stocks_news()
    n_tickers = fv.only_tickers(n['Symbol'])
    return n_tickers

# Most Active
async def most_active():
    ma = await fv.screener(signal='most_active', filters=['usa', 'mega'], order_by='-volume')
    return ma

# Most Volatile
async def most_volatile():
    mv = await fv.screener(signal='most_volatile', filters=['usa'], order_by='-marketcap')
    return mv

# Unusual volume
async def unusual_volume():
    uv = await fv.screener(signal='unusual_volume', filters=['usa'], order_by='-marketcap')
    return uv

# Call async functions
async def call_functions():

    fv_news_tickers = await news()
    fv_most_active = await most_active()
    fv_most_volatile = await most_volatile()
    fv_unusual_volume = await unusual_volume()
    fv.quit()

    fv_news_tickers.to_csv(only_tickers_path + 'news_tickers.csv', header=False)
    fv_most_active['Symbol'].to_csv(only_tickers_path + 'most_active_tickers.csv', header=False)
    fv_most_volatile['Symbol'].to_csv(only_tickers_path + 'most_volatile_tickers.csv', header=False)
    fv_unusual_volume['Symbol'].to_csv(only_tickers_path + 'unusual_volume_tickers.csv', header=False)

if __name__ == "__main__":
    asyncio.run(call_functions())
