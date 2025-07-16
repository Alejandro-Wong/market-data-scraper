import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

from important_events import important_events
from funcs import round_time


def events_to_update(file: str, all_events: dict) -> list:
    """
    Returns list of important economic calendar events that have
    occured today and need to be updated on local economic calendar 
    event history database.
    """

    # Read in latest econ calendar
    df = pd.read_csv(file, index_col=[0])

    """
    Depending on when economic calendar is saved there may be a string in the 'Time'
    column describing how many minutes until the event instead of just a time.

    example : 
        09:15,  USD,  FOMC Member Bowman Speaks  
        3 min,  USD,  Cleveland CPI (MoM) (Jun)
        12:45,  USD,  Fed Vice Chair for Supervision Barr Speaks 

    before converting 'Time' column from str format to datetime format, the 'x min'
    string must be converted to a time:

        time created + number of minutes (rounded to nearest 5 minutes if necessary)
    """

    # Get time econ cal file was created
    df_time_created = os.stat(file).st_ctime
    time_created = time.strftime("%H:%M", time.localtime(df_time_created))
    time_created = pd.to_datetime(time_created)

    # Convert any 'x min' strings to time
    df['Time'] = df['Time'].apply(
        lambda x: (
            round_time(time_created + timedelta(minutes=int(x.split(' ')[0]))).strftime('%H:%M') 
            if ':' not in x and x.split(' ')[0].isdigit() 
            else x
        )
    )

    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')

    # Check if any important events today and if they already occured
    current_time = datetime.now().replace(microsecond=0)
    current_time = pd.to_datetime(current_time)

    # Dictionary of important events today
    today_events = []
    for i, row in df.iterrows():
        if row['Event'] in all_events:
            if current_time > row['Time']:
                today_events.append(row['Event'])

    return today_events


def update_event_histories(events_codes: dict, events: list, path: str) -> None:
    """
    Iterates through all events in events list (events_to_update) and updates the event histories
    in csvs folder
    """

    for event in events:

        # URL / Headers
        url = f'https://sbcharts.investing.com/events_charts/us/{events_codes[event]}.json'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Referer': 'https://www.investing.com',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            }
        
        # Get relevant json data
        response = requests.get(url, headers=headers)

        if response.status_code == '200':
            print(f'{event} - OK!')
        else:
            print(f'{event} - ALERT!')

        response_json = response.json()
        attr = response_json['attr']

        # Create DataFrame
        df = pd.DataFrame(attr)

        if 'revised' in df.columns or 'revised_formatted' in df.columns:
            df = df.drop(columns=['revised', 'revised_formatted'])
        else:
            continue

        # df = df.dropna()

        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True).dt.tz_convert('US/Eastern').dt.date
        df = df.drop(columns='timestamp')
        df = df[['datetime','actual_state','actual','forecast']]

        df.to_csv(f'{path}{event}.csv')
        time.sleep(5)


if __name__ == "__main__":
    events = important_events()
    update_event_histories(events, [e for e in events.keys()], './csvs/')