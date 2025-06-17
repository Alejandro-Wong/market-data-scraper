import os
import time
import pytz
import pandas as pd
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import x_posts
import getpass
import importlib


class ScrapeX:
    """
        Scrape X (F.K.A Twitter) posts from specified profile(s).
    """
    def __init__(self, profiles : str | list):
        # Check for .env
        self.__check_for_env()

        # Load dotenv
        load_dotenv()

        # Instance variables
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.profiles = [profiles] if type(profiles) == str else profiles
        self.driver = webdriver.Chrome()

    def __check_for_env(self) -> None:
        """
            Checks current directory for .env containing username and password
        """
        # If .env not in current directory
        if not os.path.exists('./.env'):
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")

            # .env file content
            env = (
            f"""
            # X Login
            USERNAME={username}
            PASSWORD={password}
            """
            )

            # Write content to current directory
            with open('./.env', 'w') as f:
                f.write(env)

            # Reload module (refresh so now it detects .env)
            importlib.reload(x_posts)
        else:
            return

    def __login(self) -> None:
        """
            Login to X with credentials located in .env file
        """
        self.driver.get('https://x.com/i/flow/login')
        time.sleep(3)

        # Username
        username_input = self.driver.find_element(By.XPATH, '//input')
        username_input.send_keys(self.username)
        time.sleep(2)
        username_input.send_keys(Keys.ENTER) # Submit
        time.sleep(2)

        # Password
        password_input = self.driver.find_element(By.XPATH, '//input[@name="password"]')
        password_input.send_keys(self.password)
        time.sleep(2)
        password_input.send_keys(Keys.ENTER) # Submit
        time.sleep(2)

    def get_latest_posts(self) -> dict[str, pd.DataFrame]:
        """
            Saves the latest ~20 posts from specified profile(s) to pd.DataFrame(s)
            DataFrame(s) include(s):
                - Datetime
                - Posts
        """
        # Login
        self.__login()

        # Empty dict to store pd.DataFrames
        dfs = {}

        # Iterate through profiles
        for profile in self.profiles:

            # Get desired profile page
            self.driver.get(f'https://x.com/search?q={profile}%20-filter%3Amedia%20-filter%3Areplies%20-filter%3Aretweets%20-filter%3Aquote%20-filter%3Alinks&src=typed_query&f=live')
            time.sleep(5)

            # Empty lists for datetime and posts
            datetime_idx = []
            posts = []

            # Find posts
            latest_posts = self.driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

            # Separate a clean datetime and post info, append to appropriate lists
            for post in latest_posts:
                time_tag = post.find_element(By.XPATH, './/time')
                datetime_attr = pd.to_datetime(time_tag.get_attribute('datetime'))
                datetime = datetime_attr.tz_convert(pytz.timezone('America/New_York'))
                datetime = datetime.strftime('%Y-%m-%d %H:%M')
                datetime = pd.to_datetime(datetime)
                datetime_idx.append(datetime)

                filter_text = post.text.splitlines()
                text = filter_text[4]
                posts.append(text)

            # Create dataframe of latest posts
            datetime_series = pd.Series(datetime_idx)
            posts_series = pd.Series(posts)

            df_dict = {'Datetime':datetime_series, 'Posts':posts_series}
            df = pd.DataFrame(df_dict)

            # Add DataFrame to dictionary
            dfs[profile] = df

        self.driver.close()

        return dfs


