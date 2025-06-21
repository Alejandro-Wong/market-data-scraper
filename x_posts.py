import os
import time
import pytz
import pandas as pd
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains 

import x_posts
import getpass
import importlib

class XPosts:
    """
        Scrape X (F.K.A Twitter) posts from specified profile(s).
    """
    def __init__(self, profiles : str | list = None, headless : bool = False):
        # Check for .env
        self.__check_for_env()

        # Load dotenv
        load_dotenv()

        # Instance variables
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.profiles = [profiles] if type(profiles) == str else profiles
        self.options = Options()
        self.headless = headless

        if self.headless:
            self.options.add_argument("--headless")

        # User Agent
        self.options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")

        # Driver
        self.driver = webdriver.Chrome(options=self.options)

        # Login
        self.__login()

    def __check_for_env(self) -> None:
        """
            Checks current directory for .env containing username and password
        """
        # If .env not in current directory
        if not os.path.exists('./.env'):
            username = input("Enter X username: ")
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
        username_input.send_keys(self.username) if self.username else None
        time.sleep(2)
        username_input.send_keys(Keys.ENTER) # Submit
        time.sleep(2)

        # Password
        password_input = self.driver.find_element(By.XPATH, '//input[@name="password"]')
        password_input.send_keys(self.password) if self.password else None
        time.sleep(2)
        password_input.send_keys(Keys.ENTER) # Submit
        time.sleep(2)

    def get_latest_posts(self, profile : str) -> pd.DataFrame:
        """
            Saves the latest ~20 posts from specified profiles(s) to pd.DataFrame(s)
            DataFrame(s) include(s):
                - Datetime
                - Posts
        """
        # Get desired profiles page
        self.driver.get(f'https://x.com/search?q={profile}%20-filter%3Amedia%20-filter%3Areplies%20-filter%3Aretweets%20-filter%3Aquote%20-filter%3Alinks&src=typed_query&f=live')
        time.sleep(3)

        # User not found
        not_found = self.driver.find_elements(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div[1]/span')
        if not_found:
            print(f"{profile} not found, check spelling")
            return
        
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

        return df
    
    def get_media(self, path : str) -> None:
        """
            Due to inability to download urls from X/Twitter (Status Code: 300) pictures must be
            saved by doing full page screenshots. Since webdriver.Chrome() doesn't support
            this function, driver must be switched from .Chrome() to .FireFox()

            Args:
            - path (file path to save pictures to) : str
        """
        # Change Driver and options
        # ffox_options = Options()

        # if self.headless:
        #     ffox_options.add_argument("--headless")

        # User Agent
        # ffox_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 14.7; rv:139.0) Gecko/20100101 Firefox/139.0")

        self.driver = webdriver.Firefox()

        # Login
        self.__login()

        # Action Chains
        action = ActionChains(self.driver)

        # Iterate through profiles
        for profiles in self.profiles:

            # Get Profile/Media
            self.driver.get(f'https://x.com/{profiles}/media')
            time.sleep(3)

            # Media section thumbnails
            media_section = self.driver.find_elements(By.XPATH, '//*[@role="listitem"]/div/div/div/a/div/div[2]/div/img')

            # Store pics and vids thumbnail urls separately
            pic_ids = []
            vids = []

            """
            pic thumbnail URL example : https://pbs.twimg.com/media/Gtuffc0WEAEppQ4?format=jpg&name=360x360
            vid thumbnail URL example : https://pbs.twimg.com/amplify_video_thumb/1935194033569103872/img/6_w1b9-jUkgcldUq?format=jpg&name=360x360
            """

            # Iterate through media thumbnails, separate pics and vids
            for media in media_section:
                url = media.get_attribute('src')
                if url[22:27] == "media":
                    pic_ids.append(url[28:43])
                else:
                    vids.append(url)

            # Save images
            full_size = "4096x4096"
            # full_size2 = "large"
            for id, i in zip(pic_ids, range(len(pic_ids))):
                
                # Reconstruct pic URLS to be able to save full sized pictures
                self.driver.get(f'https://pbs.twimg.com/media/{id}?format=jpg&name={full_size}')
                time.sleep(2)
                pic = self.driver.find_element(By.XPATH, "/html/body/img")
                pic.click()
                time.sleep(1)
                self.driver.get_full_page_screenshot_as_file(f'{path}/{profiles}_{i}.png')
                time.sleep(1)

        self.driver.close()


