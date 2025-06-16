import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

"""
Fetches: 
    - Seconds/minutes since posted
    - Headline
    - Ticker
    - Percentage up or down (optional)
    - Source


To do:
    find a way to better organize data
"""


def finviz_stocks_news():
    url : str = 'https://finviz.com/news.ashx?v=3'

    # Disable popup
    option = Options()
    # option.add_argument("--headless")
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2}
    )

    # Driver
    driver = webdriver.Chrome(options=option)

    # Finviz News/Stocks News
    driver.get(url)

    time.sleep(3)
    table  = driver.find_elements(By.XPATH, '//*[@id="news"]/div/table/tbody/tr')
    table_list = []

    for i in range(len(table)):
        table_list.append(table[i].text.splitlines())

    minutes = []
    headlines = []
    tickers = {}
    sources = []

    for row, i in zip(table_list, range(len(table_list))):
        minutes.append(row[0])
        headlines.append(row[1])
        sources.append(row[-1])
        if row[2] != row[-2]:
            tickers[i] = row[2:-2]
        else:
            tickers[i] = row[2]

    print(minutes)
    print(headlines)
    print(tickers)
    print(sources)