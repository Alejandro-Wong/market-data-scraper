import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

from finviz import Finviz
from tables import table
import pandas as pd
import asyncio


load_dotenv()

# Token
token = os.getenv('DISCORD_TOKEN')

# Log Handler
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot online')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

# Paths
full_table_screener_csvs = './csvs/full_tables/screeners/'
full_table_screener_pngs = './pngs/full_tables/screeners/'

# Screener Start / Time til refresh
screener_start = False
screener_delay = 60 * 5


async def finviz_screeners(channel: discord.TextChannel):

    print("FinViz Screeners Activated","\n")

    # Global start variable
    global screener_start
    
    # Column widths for table
    columnwidth = [25, 70, 70, 70, 70]

    while screener_start == True:
        # FinViz Scraper
        fz = Finviz()

        # Screeners
        print("Fetching Screeners...","\n")
        most_active = await fz.screener(signal='most_active', filters=['usa', 'mega'], order_by='-volume')
        most_volatile = await fz.screener(signal='most_volatile', filters=['usa'], order_by='-marketcap')
        unusual_volume = await fz.screener(signal='unusual_volume', filters=['usa'], order_by='-marketcap')
       
        # Send tables to csv
        print("Exporting to CSV...","\n")
        most_active.to_csv(full_table_screener_csvs + 'most_active.csv')
        most_volatile.to_csv(full_table_screener_csvs + 'most_volatile.csv')
        unusual_volume.to_csv(full_table_screener_csvs + 'unusual_volume.csv')

        # Quit browser
        fz.quit()

        # Read / Clean CSV Dataframes, Export tables as PNG
        print("Cleaning CSVs, Exporting tables as PNG...","\n")
        for filename in os.listdir(full_table_screener_csvs):
            df = pd.read_csv(f"{full_table_screener_csvs}{filename}")
            if filename == 'news_headlines.csv':
                continue
            else:
                df = df[['Symbol','Company','Market Cap','Price','Volume']]
                table(df, filename[:-4], columnwidth, full_table_screener_pngs)
        
        # Send PNG of tables to channel
        print("Sending PNGs to chat...","\n")
        for filename in os.listdir(full_table_screener_pngs):
            if filename == 'news_headlines.png':
                continue
            else:
                await channel.send(file=discord.File(f'{full_table_screener_pngs}{filename}'))
        
        # Run again every x minutes
        print(f"Waiting {int(screener_delay / 60)} minute(s) to refresh screeners...","\n")
        await asyncio.sleep(screener_delay)

# News start / Time til refresh
news_start = False
news_delay = 60 * 5

async def finviz_news(channel: discord.TextChannel):

    print("FinViz News Headlines activated")
    # Global start variable
    global news_start

    # Column widths for table
    columnwidth = [25, 200, 25, 25]
    
    while news_start == True:

        fz = Finviz()
        news = await fz.stocks_news()

        # Send table to csv
        print("Exporting to CSV...","\n")
        news.to_csv(full_table_screener_csvs + 'news_headlines.csv')

        # Read / Clean CSV, Export tables as PNG
        df = pd.read_csv(f'{full_table_screener_csvs}news_headlines.csv', index_col=[0])
        table(df, 'news_headlines', columnwidth, full_table_screener_pngs)

        # Send PNG to channel
        print("Sending PNG to chat...","\n")
        await channel.send(file=discord.File(f'{full_table_screener_pngs}news_headlines.png'))

        # Run again every x minutes
        print(f"News headlines will refresh in {int(news_delay / 60)} minute(s)...")
        await asyncio.sleep(news_delay)
    

# !start_screeners
@bot.command()
async def start_screeners(channel: discord.TextChannel):
    global screener_start
    if screener_start == False:
        screener_start = True
        await channel.send('Activating FinViz Screeners')
        await finviz_screeners(channel)
    else:
        await channel.send('FinViz Screeners already activated')

# !stop_screeners
@bot.command()
async def stop_screeners(channel: discord.TextChannel):
    global screener_start
    if screener_start == True:
        screener_start = False
        await channel.send('FinViz Screeners stopped')
    else:
        await channel.send('Screeners already stopped')

# !start_news
@bot.command()
async def start_news(channel: discord.TextChannel):
    global news_start
    if news_start == False:
        news_start = True
        await channel.send('Activating FinViz News Headlines')
        await finviz_news(channel)
    else:
        await channel.send('FinViz News Headlines already activated')

# !stop_news
@bot.command()
async def stop_news(channel: discord.TextChannel):
    global news_start
    if news_start == True:
        news_start = False
        await channel.send('FinViz News Headlines stopped')
    else:
        await channel.send('News Headlines already stopped')

# !clear
@bot.command()
async def clear(ctx):
    await ctx.channel.purge()

bot.run(token, log_handler=handler)