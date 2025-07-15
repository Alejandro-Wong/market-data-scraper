import os
import re
import time
import asyncio
import pandas as pd
from dotenv import load_dotenv

from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains 

ua = UserAgent()


class InvestingCom:
    def __init__(self, headless: bool=True):

        # Load dotenv
        load_dotenv()

        # Instance variables
        self.username = os.getenv("email")
        self.password = os.getenv("password")
        self.headless = headless

        # Options
        self.option = Options()

        # If headless True
        if self.headless:
            self.option.add_argument("--headless=new")

        self.option.add_argument("--disable-gpu")

        # Disable popups and extensions (hopefully)
        self.option.add_argument("--disable-infobars")
        self.option.add_argument("start-maximized")
        self.option.add_argument("--disable-extensions")
        self.option.page_load_strategy = 'none'

        # Pass the argument 1 to allow and 2 to block
        self.option.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 2}
        )
        
        # User agent
        self.option.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")
        # self.option.add_argument(f"--user-agent={ua.chrome}")

        # Driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.option)


    async def econ_calendar(self, filter: str='USD'):

        # URL 
        url = "https://www.investing.com/economic-calendar/"
        self.driver.get(url)
        await asyncio.sleep(2)

        table = self.driver.find_element(By.XPATH, '//*[@id="economicCalendarData"]')

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
    

test = InvestingCom()

async def econ_cal():
    await test.econ_calendar()

if __name__ == "__main__":
    asyncio.run(econ_cal())
