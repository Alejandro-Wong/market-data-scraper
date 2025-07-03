import pandas as pd
import re
from extract_tickers import only_tickers
import ast

test = pd.read_csv('./ttv_625.csv', index_col=[0])
test['Datetime'] = pd.to_datetime(test['Datetime']).dt.date

date = test['Datetime']
# date = pd.to_datetime(date).dt.date
posts = test['Posts']
# print(posts)

sticky_notes = {}

for i, row in test.iterrows():
    str_to_list = ast.literal_eval(row['Posts'])
    date = str(row['Datetime'])

    ticker_trade = []
    for item in str_to_list:
        if '$' in item:
            start = item.find('$')
            end = item.find(':')
            ticker_trade.append(item[start:end])
    

    ticker = only_tickers(ticker_trade)
    trade = []
    for item in ticker_trade:
        start = item.find('(')
        end = item.find(')')
        trade.append(item[start+1:end])
    
    ticker_series = pd.Series(ticker)
    trade_series = pd.Series(trade)

    df_dict = {'Ticker': ticker_series, 'Entry': trade_series}
    df = pd.DataFrame(df_dict)

    sticky_notes[date] = df

print(sticky_notes)
# for df in sticky_notes:
#     print(sticky_notes[df])




# # Convert string to list
# str_to_list = ast.literal_eval(sample)


# print(ticker_trade)








# split_1 = re.split(r"[$]", sample)
# split_2 = re.split(r"[.]", sample)


# tickers = only_tickers(split_2)
# trade = []
# description = []

# for i in split_1:
#     if '(' in i:
#         op_par = i.find('(')
#         cl_par = i.find(')')
#         description.append(i[op_par+1:cl_par])

# print(split_1)
# print(tickers)
# print(description)






