import discord
from discord.ext import tasks, commands
import logging
from dotenv import load_dotenv
import os

from finviz.finviz import Finviz
from discord_bot.tables import table
import pandas as pd
import time

load_dotenv()

# Token
token = os.getenv('DISCORD_TOKEN')

# Handler
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Client
client = discord.Client(intents=intents)
# channel = client.get_channel(1389614253174165527


# Paths
full_table_path = './csvs/full_tables/'
full_table_screener_csvs = './csvs/full_tables/screeners/'
full_table_screener_pngs = './pngs/full_tables/screeners/'

# # Bot Commands
# bot = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Bot Online')
    if not send_png.is_running():
        channel = await client.fetch_channel(1389614253174165527)
        send_png.start(channel)

# Send png to chat
@tasks.loop(minutes=5)
async def send_png(channel: discord.TextChannel):
    # FinViz Scraper
    fz = Finviz()

    # Screener
    most_active = fz.screener(signal='most_active', filters=['nyse'], order_by='-volume')
    most_volatile = fz.screener(signal='most_volatile', filters=['nyse'], order_by='-volume')
    unusual_volume = fz.screener(signal='unusual_volume', filters=['nyse'], order_by='-volume')
    
    # Send tables to csv 
    most_active.to_csv(full_table_screener_csvs + 'most_active.csv')
    most_volatile.to_csv(full_table_screener_csvs + 'most_volatile.csv')
    unusual_volume.to_csv(full_table_screener_csvs + 'unusual_volume.csv')

    for filename in os.listdir(full_table_screener_csvs):
        df = pd.read_csv(f"{full_table_screener_csvs}{filename}")
        df = df[['Symbol','Company','Market Cap','Price','Volume']]
        table(df, filename[:-4], full_table_screener_pngs)
    
    for filename in os.listdir(full_table_screener_pngs):
        await channel.send(file=discord.File(f'{full_table_screener_pngs}{filename}'))

@client.event
async def on_ready():
    if not send_png.is_running():
        channel = await client.fetch_channel(1389614253174165527)
        send_png.start(channel)

# bot.run(token)
client.run(token)
    
