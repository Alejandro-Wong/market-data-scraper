import pandas as pd
from finviz import Finviz

fz = Finviz()

news = fz.stocks_news()
screener = fz.screener('most_active', ['usa','mega'], '-marketcap')

print(news)
print(screener)