from datetime import datetime, timedelta

def important_events() -> dict:
    """
    Returns dictionary of mostly 3 star and some 2 star economic calendar events
    that can be found on the current week's economic calendar on investing.com

    Keys: Economic calendar events
    Values: Database IDs
    """
    # Get current and previous month names.
    today = datetime.now()
    curr_mo = today.strftime('%B')[:3]

    first_day = today.replace(day=1)
    previous_month = first_day - timedelta(days=1)
    prev_mo = previous_month.strftime('%b')

    # Events : Event id
    events_id = {
        'Crude Oil Inventories': 75,
        f'Core CPI (YoY) ({prev_mo})': 736,
        f'CPI (YoY) ({prev_mo})': 733,
        f'Core CPI (MoM) ({prev_mo})': 56,
        f'PPI (MoM) ({prev_mo})': 238,
        f'Core Retail Sales (MoM) ({prev_mo})': 63,
        f'Retail Sales (MoM) ({prev_mo})': 256,
        'Initial Jobless Claims': 294,
        f'Michigan 1-Year Inflation Expectations ({curr_mo})': 389,
        f'Michigan Consumer Sentiment ({curr_mo})': 320,
        f'Philadelphia Fed Manufacturing Index ({curr_mo})': 236,
        f'Existing Home Sales ({prev_mo})': 99,
        f'New Home Sales ({prev_mo})': 222,
        f'Durable Goods Orders (MoM) ({prev_mo})': 86,
        # f'S&P Global Manufacturing PMI ({curr_mo})': 829,
        # f'S&P Global Services PMI ({curr_mo})': 1062,
        f'CB Consumer Confidence ({curr_mo})': 48,
        f'JOLTS Job Openings ({prev_mo})': 1057,
        f'ADP Nonfarm Employment Change ({curr_mo})': 1,
        f'GDP (QoQ) (Q2)': 375,
        'Fed Interest Rate Decision': 168,
        f'Core PCE Price Index (YoY) ({prev_mo})': 905,
        f'Core PCE Price Index (MoM) ({prev_mo})': 61,
        f'Average Hourly Earnings (MoM) ({curr_mo})': 8,
        f'Nonfarm Payrolls ({curr_mo})': 227,
        f'Unemployment Rate ({curr_mo})': 300,
    }

    return events_id