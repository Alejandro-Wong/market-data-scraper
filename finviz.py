import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import screener_params as sp

class Finviz:

    def __init__(self, headless: bool = True):

        # Instance variables
        self.headless = headless
        
        # Options
        self.option = Options()

        # If headless True
        if self.headless:
            self.option.add_argument("--headless")

        # Disable popups and extensions (hopefully)
        self.option.add_argument("--disable-infobars")
        self.option.add_argument("start-maximized")
        self.option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        self.option.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 2}
        )
        
        # User agent
        self.option.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")

        # Driver
        self.driver = webdriver.Chrome(options=self.option)

        # Screener Signals
        self.signals = [
            'ta_topgainers','ta_toplosers','ta_newhigh','ta_newlow','ta_mostvolatile','ta_mostactive','ta_unusualvolume',
            'ta_overbought','ta_oversold','n_downgrades','n_upgrades,','n_earningsbefore','n_earningsafter','it_latestbuys',
            'it_latestsells','n_majornews','ta_p_horizontal','ta_p_tlresistance','ta_p_tlsupport','ta_p_wedgeup','ta_p_wedgedown',
            'ta_p_wedgeresistance','ta_p_wedgesupport','ta_p_wedge','ta_p_channelup','ta_p_channeldown','ta_p_channel','ta_p_doubletop',
            'ta_p_doublebottom','ta_p_multipletop','ta_p_multiplebottom','ta_p_headandshoulders','ta_p_headandshouldersinv'
        ]

        # Screener columns for 'order by'
        self.columns = ['ticker','company','sector','industry','country','marketcap','pe','price','change','volume']

    def stocks_news(self) -> pd.DataFrame:
        """
            Latest stock related headlines
            Includes:
                - Seconds/Minutes since posted
                - Headline
                - Ticker(s)
                - Source
        """

        # URL
        url = 'https://finviz.com/news.ashx?v=3'
        self.driver.get(url)
        time.sleep(2)

        # Table
        table  = self.driver.find_elements(By.XPATH, '//*[@id="news"]/div/table/tbody/tr')

        # Rows
        table_list = []
        for i in range(len(table)):
            table_list.append(table[i].text.splitlines())

        # Lists for data separation
        minutes = []
        headlines = []
        tickers = []
        sources = []
        
        # Append lists with data
        for row, i in zip(table_list, range(len(table_list))):
            minutes.append(row[0])
            headlines.append(row[1])
            sources.append(row[-1])
            if row[2] != row[-2]:
                tickers.append(', '.join(row[2:-2]))
            else:
                tickers.append(row[2])

        # DataFrame
        min_series = pd.Series(minutes)
        headline_series = pd.Series(headlines)
        ticker_series = pd.Series(tickers)
        source_series = pd.Series(sources)

        df_dict = {'Time':min_series, 'Headline':headline_series, 'Symbol':ticker_series, 'Source':source_series}
        df = pd.DataFrame(df_dict)

        return df
    
    def __url(self, signal: str=None, filters: list[str]=None, order_by: str=None) -> str:
        """
            Constructs URL for screener by adding all applicaple parameters to a list.
            Returns joined list for final URL
        """
        url_parts = [sp.base_url]

        # Signal
        if signal:
            url_parts.extend([sp.signal_query, sp.signals[signal]])
        
        # Filters
        if filters:
            url_parts.append(sp.filter_query)

            if len(filters) == 1:
                url_parts.append(sp.search_filters(filters[0]))
            elif len(filters) == 2:
                url_parts.extend([sp.search_filters(filters[0]), sp.comma, sp.search_filters(filters[1])])
            else:
                url_parts.append(sp.search_filters(filters[0]))
                for filter in filters[1:]:
                    url_parts.append(sp.comma_multi)
                    url_parts.append(sp.search_filters(filter))
        # Order
        if order_by:
            url_parts.extend([sp.order_query, order_by])

        return ''.join(url_parts)
    
  
    def screener(self, signal: str=None, filters: list[str]=None, order_by: str=None) -> pd.DataFrame:
        """
            DataFrame of Finviz free screener results. 
            For now, only allows filtering by Signal (list of pre-made signals)
            and ordering results by columns.
        """

        url = self.__url(signal, filters, order_by)

        self.driver.get(url)
        time.sleep(15)
        screener_table = self.driver.find_elements(By.XPATH, '//*[@id="screener-table"]/td/table/tbody/tr/td/table/tbody/tr')
        table = []
        for row in screener_table:
            table.append(row.text.splitlines())

        columns = ['#','Symbol','Company','Sector','Industry','Country','Market Cap','P/E','Price','Change','Volume']

        df = pd.DataFrame(table, columns=columns)
        df = df.set_index('#')

        return df