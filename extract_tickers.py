import pandas as pd
import re

def only_tickers(col: pd.Series) -> list:
    """
        Iterates through DataFrame column and finds
        all instances of tickers i.e '$AAPL', '$XYZ'.
        Appends tickers to a list.
    """

    # Regex pattern to find tickers prefixed by '$'
    pattern = r'\$([A-Z^]+)'

    # Tickers list
    tickers = []
    
    # Append only unique tickers (no duplicates)
    for strings in col:
        split = strings.split(' ')
        for string in split:
            # Isolate ticker
            if re.search(pattern, string):
                # Remove $ from ticker, then remove any punctuation
                target = string[1:]
                target = re.sub(r'[^\w\s]','', target)
                if target not in tickers:
                    tickers.append(target)


    return tickers

def popular_tickers(tickers: list[list] | list) -> pd.DataFrame:
    """
        Combines multiple lists of tickers, counts number
        of instances of each ticker. Returns DataFrame showing
        tickers in order by popularity.
    """

    ticker_count = {}

    if type(tickers) == list:
        # If list of lists
        if isinstance(tickers[0], list):
            for _list in tickers:
                for ticker in _list:
                    if ticker not in ticker_count:
                        ticker_count[ticker] = 1
                    else:
                        ticker_count[ticker] += 1
        # If just list
        elif isinstance(tickers[0], str):
            for ticker in tickers:
                # If multiple tickers in row
                if ',' in ticker:
                    print(ticker)
                    split = ticker.split(',')
                    for i in split:
                        print(i)
                        if i not in ticker_count:
                            ticker_count[i] = 1
                        else:
                            ticker_count[i] += 1
                elif ticker not in ticker_count:
                    ticker_count[ticker] = 1
                else:
                    ticker_count[ticker] += 1
    else:
        raise TypeError("Argument must be a list or list of lists")

    # Construct DataFrame
    ticker_series = pd.Series(ticker_count.keys())
    count_series = pd.Series(ticker_count.values())

    df_dict = {'Ticker': ticker_series, 'Count': count_series}

    df = pd.DataFrame(df_dict)
    df = df.sort_values(by='Count', ascending=False) # Sort highest to lowest

    return df
    
    

