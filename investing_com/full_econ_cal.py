import requests
import pandas as pd
from bs4 import BeautifulSoup
from network_requests import headers, cookies, data

def full_econ_calendar() -> pd.DataFrame:
    """
    Investing.com Economic Calendar for the current week
    """

    url = 'https://www.investing.com/economic-calendar/Service/getCalendarFilteredData'
    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    if response.status_code != 200:
        print(response.status_code)

    json = response.json()['data']
    soup = BeautifulSoup(json, 'html.parser')

    dates = [date.text for date in soup.find_all('td', { 'class': 'theDay' })]
    times = [time.text for time in soup.find_all('td', { 'class': 'first'})]
    curr = [cur.text[-3:] for cur in soup.find_all('td', { 'class': 'flagCur'})]
    stars = [star for star in soup.find_all('td', { 'class': 'sentiment', 'data-img_key': True})]
    num_stars = []
    for star in stars:
        img_key = star.get('data-img_key')
        num_stars.append(int(img_key[4]))
    events = [event.text.strip() for event in soup.find_all('td', { 'class': 'event'})]

    df = pd.DataFrame()
    df['Time'] = pd.to_datetime(pd.Series(times), format="%H:%M").dt.time
    df['Country'] = pd.Series(curr)
    df['Stars'] = pd.Series(num_stars)
    df['Event'] = pd.Series(events)

    df['Date'] = dates[0] 
    c = 0
    for i in range(1, len(df)):
        current_time = df.loc[i, 'Time']
        prev_time = df.loc[i - 1, 'Time']

        if current_time < prev_time and c < len(dates):
            c += 1
        
        df.loc[i, 'Date'] = dates[c]

    df = df[['Date','Time','Country','Stars','Event']]
    df.to_csv('./csvs/full_econ_calendar.csv')
    
    return df


if __name__ == "__main__":
    full_econ_calendar()

                                                                                                                                                                    