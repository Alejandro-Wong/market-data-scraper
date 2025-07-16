import asyncio
import pandas as pd


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


async def econ_calendar(filter: str='USD') -> pd.DataFrame:
    """
    Fetches today's economic calendar from investing.com filters by currency, filter
    set to USD by default.
    """

    # Options
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.page_load_strategy = 'none'

    # User agent
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")

    # Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL 
    url = "https://www.investing.com/economic-calendar/"
    driver.get(url)
    await asyncio.sleep(2)

    # Table
    table = driver.find_element(By.XPATH, '//*[@id="economicCalendarData"]')

    # Columns
    time = table.find_elements(By.XPATH, '//*[@class="first left time js-time"]')
    cur = table.find_elements(By.XPATH, '//*[@class="left flagCur noWrap"]')
    importance = table.find_elements(By.XPATH, '//*[@class="left textNum sentiment noWrap"]')
    event = table.find_elements(By.XPATH, '//*[@class="left event"]')

    # Series
    cur_series = pd.Series([c.text for c in cur])
    time_series = pd.Series([t.text for t in time]) 
    event_series = pd.Series([e.text for e in event])

    # DataFrame
    df = pd.DataFrame()
    df['Time'] = time_series
    df['Country'] = cur_series
    df['Event'] = event_series

    return df[df['Country'].str.strip() == filter]

# Save df to csv
async def save_econ_cal():
    cal = await econ_calendar()
    cal.to_csv('./csvs/econ_calendar.csv')

if __name__ == "__main__":
    asyncio.run(save_econ_cal())
