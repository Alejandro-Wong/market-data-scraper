from x_posts import XPosts
from finviz import Finviz
from tables import table
import pandas as pd

from extract_tickers import *

import os

# df = pd.read_csv('./csvs/full_tables/most_active.csv')
# df = df[['Symbol','Company','Market Cap','Price','Volume']]
# table(df, 'Finviz Most Active')

full_table_screener_csvs = './csvs/full_tables/screeners/'
full_table_screener_pngs = './pngs/full_tables/screeners/'


for filename in os.listdir(full_table_screener_csvs):
    df = pd.read_csv(f"{full_table_screener_csvs}{filename}")
    df = df[['Symbol','Company','Market Cap','Price','Volume']]
    table(df, filename[:-4], full_table_screener_pngs)

# # CSV Paths
# full_table_path = './csvs/full_tables/'
# only_tickers_path = './csvs/only_tickers/'

# # Finviz
# fv = Finviz()

# ## NEWS HEADLINES ##

# # Stocks News
# news = fv.stocks_news()
# news_tickers = fv.only_tickers(news['Symbol'])



# ## SCREENER ## 

# # Most Active
# most_active = fv.screener(signal='most_active', filters=['nyse'], order_by='-marketcap')

# # Most Volatile
# most_volatile = fv.screener(signal='most_volatile', filters=['nyse'], order_by='-marketcap')

# # Unusual volume
# unusual_volume = fv.screener(signal='unusual_volume', filters=['nyse'], order_by='-marketcap')



# ## CSVS ## 

# # Send tables to csv
# news.to_csv(full_table_path + 'news.csv')
# most_active.to_csv(full_table_path + 'most_active.csv')
# most_volatile.to_csv(full_table_path + 'most_volatile.csv')
# unusual_volume.to_csv(full_table_path + 'unusual_volume.csv')

# # Send tickers to csv
# news_tickers.to_csv(only_tickers_path + 'news_tickers.csv', header=False)
# most_active['Symbol'].to_csv(only_tickers_path + 'most_active_tickers.csv', header=False)
# most_volatile['Symbol'].to_csv(only_tickers_path + 'most_volatile_tickers.csv', header=False)
# unusual_volume['Symbol'].to_csv(only_tickers_path + 'unusual_volume_tickers.csv', header=False)































# profiles = ['FirstSquawk', 'unusual_whales', 'StockMKTNewz', 'RealDyTrading']
# x = XPosts()

# Latest posts for each profile
# fs = x.get_latest_posts('FirstSquawk')s
# uw = x.get_latest_posts('unusual_whales')
# s_mkt = x.get_latest_posts('StockMKTNewz')
# rdt = x.get_latest_posts('RealDayTrading')
# ttv = x.get_posts('tradertvshawn', keywords=["Here's what"], exclude=['replies','quote'])
# rdt = x.get_posts('RealDayTrading')

# ttv.to_csv('./ttv_626.csv')

# print(ttv)
# print(rdt)
# print(fs)
# print(uw)
# print(s_mkt)


# Extract only tickers mentioned by each profile
# fs_tickers = only_tickers(fs['Posts'])
# uw_tickers = only_tickers(uw['Posts'])
# s_mkt_tickers = only_tickers(s_mkt['Posts'])
# rdt_tickers = only_tickers(rdt['Posts'])

# All profiles ticker mentions value counts
# pop_tickers = popular_tickers([fs_tickers, uw_tickers, s_mkt_tickers, rdt_tickers])
# print(pop_tickers)

# # Finviz
# fv = Finviz(headless=False)

# # News headlines
# news = fv.stocks_news()

# # Screener : Most Active ordered by highest marketcapw
# most_active_by_marketcap = fv.screener('most_active',['mega','sp500'],'-marketcap')
# print(news)
# print(most_active_by_marketcap)

# # All tickers mentioned in news headlines
# fz_tickers = news['Symbol']

# # News tickers values counts
# fz_pop_tickers = popular_tickers([ticker for ticker in fz_tickers])
# print(fz_pop_tickers.to_string())


