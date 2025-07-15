import requests
import datetime
import pandas as pd 
import time

event_codes = {
    "crude_oil_inventories": 75,
    "core_cpi_yoy": 736,
    "cpi_yoy": 733,
    "core_cpi_mom": 56,
    "ppi_mom": 238,
    "core_retail_sales": 63,
    "retail_sales": 256,
    "initial_jobless": 294,
    "inflation_expectations_1yr": 389,
    "consumer_sentiment": 320
}

def get_event_histories(events_codes: dict):
    for event in event_codes.keys():

        url = f'https://sbcharts.investing.com/events_charts/us/{event_codes[event]}.json'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Referer': 'https://www.investing.com',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            }
        
        # Get relevant json data
        response = requests.get(url, headers=headers)
        print(f'{event} - {response.status_code}')
        response_json = response.json()
        attr = response_json['attr']

        # Create DataFrame
        df = pd.DataFrame(attr)
        df = df.drop(columns=['revised', 'revised_formatted'])
        df = df.dropna()

        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True).dt.tz_convert('US/Eastern').dt.date
        df = df.drop(columns='timestamp')
        df = df[['datetime','actual_state','actual','forecast']]

        df.to_csv(f'./csvs/event_history/{event}.csv')
        time.sleep(5)

if __name__ == "__main__":
    get_event_histories(event_codes)