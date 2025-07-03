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

# Start condition / timer delay
start = False
delay = 60 * 5


async def finviz_screeners(channel: discord.TextChannel):


    print("FinViz Screeners Activated","\n")

    global start
    while start == True:
        # FinViz Scraper
        fz = Finviz()

        # Screeners
        print("Fetching Screeners...","\n")
        most_active = await fz.screener(signal='most_active', filters=['usa', 'mega'], order_by='-volume')
        most_volatile = await fz.screener(signal='most_volatile', filters=['usa'], order_by='-marketcap')
        unusual_volume = await fz.screener(signal='unusual_volume', filters=['usa'], order_by='-marketcap')

        print("Fetching Latest News")
        news = await fz.stocks_news()
        
        # Send tables to csv
        print("Exporting to CSV...","\n")
        most_active.to_csv(full_table_screener_csvs + 'most_active.csv')
        most_volatile.to_csv(full_table_screener_csvs + 'most_volatile.csv')
        unusual_volume.to_csv(full_table_screener_csvs + 'unusual_volume.csv')
        news.to_csv(full_table_screener_csvs + 'news.csv')

        # Quit browser
        fz.quit()

        # Read / Clean CSV Dataframes, Export tables as PNG
        print("Cleaning CSVs, Exporting tables as PNG...","\n")
        for filename in os.listdir(full_table_screener_csvs):
            df = pd.read_csv(f"{full_table_screener_csvs}{filename}")
            if filename == 'news.csv':
                table(df[:10], filename[:-4], full_table_screener_pngs)
            else:
                df = df[['Symbol','Company','Market Cap','Price','Volume']]
                table(df, filename[:-4], full_table_screener_pngs)
        
        # Send PNG of tables to channel
        print("Sending PNGs to chat...","\n")
        for filename in os.listdir(full_table_screener_pngs):
            await channel.send(file=discord.File(f'{full_table_screener_pngs}{filename}'))
        
        # Run again every x minutes
        print(f"Waiting {delay / 60} minute(s) to refresh screeners...","\n")
        await asyncio.sleep(delay)

# !start_screeners
@bot.command()
async def start_screeners(channel: discord.TextChannel):
    global start
    if start == False:
        start = True
        await channel.send('Activating FinViz Screeners')
        await finviz_screeners(channel)
    else:
        await channel.send('FinViz Screeners already activated')

# !stop_screeners
@bot.command()
async def stop_screeners(channel: discord.TextChannel):
    global start
    if start == True:
        start = False
        await channel.send('FinViz Screeners Stopped')
    else:
        await channel.send('Screeners already stopped')

bot.run(token, log_handler=handler)