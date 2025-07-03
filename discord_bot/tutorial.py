import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os



"""
To deploy the bot (have it running indefinitely) you can use 'Render' https://render.com/
"""


load_dotenv()

# Token
token = os.getenv('DISCORD_TOKEN')

# Handler
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# # Bot
# bot = commands.Bot(command_prefix='!', intents=intents)

# Client
client = discord.Client(intents=intents)
channel = client.get_channel(1389614253174165527)

@tasks.loop(seconds=10)
async def auto_send(channel : discord.TextChannel):
    await channel.send('Test Message')

@client.event
async def on_ready():
    if not auto_send.is_running():
        channel = await client.fetch_channel(1389614253174165527)
        auto_send.start(channel)

client.run(token)








# # Roles
# role1 = "Executioner"

# # Events
# @bot.event
# async def on_ready():
#     print(f"We are ready to go in, {bot.user.name}")
#     if not auto_send.is_running():
#         channel = await client.fetch_channel(1389614253174165527)
#         auto_send.start(channel)
#     print('Ready')

# @bot.event
# async def on_member_join(member):
#     await member.send(f"Welcome to the server {member.name}")

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return 
    
#     if "shit" in message.content.lower():
#         await message.delete()
#         await message.channel.send(f"{message.author.mention} no cursing on this server please")

#     await bot.process_commands(message)


# # Commands

# # !hello
# @bot.command()
# async def hello(ctx):
#     await ctx.send(f"Hello {ctx.author.mention}!")

# # !assign
# @bot.command()
# async def assign(ctx):
#     role = discord.utils.get(ctx.guild.roles, name=role1)
#     if role:
#         await ctx.author.add_roles(role)
#         await ctx.send(f"{ctx.author.mention} is now assigned to {role1}")
#     else:
#         await ctx.send("Role doesn't exist")

# # !remove
# @bot.command()
# async def remove(ctx):
#     role = discord.utils.get(ctx.guild.roles, name=role1)
#     if role:
#         await ctx.author.remove_roles(role)
#         await ctx.send(f"{ctx.author.mention} is no longer {role1}")
#     else:
#         await ctx.send("Role doesn't exist")

# # !secret 
# @bot.command()
# @commands.has_role(role1)
# async def secret(ctx):
#     await ctx.send("Welcome to the club!")

# @secret.error
# async def secret_error(ctx, error):
#     if isinstance(error, commands.MissingRole):
#         await ctx.send("You don't have permission to do that")

# # !dm
# @bot.command()
# async def dm(ctx, *, msg):
#     await ctx.author.send(f"Private Message: {msg}")

# # !reply
# @bot.command()
# async def reply(ctx):
#     await ctx.reply("This is reply to message")


# # Tasks
# @tasks.loop(seconds=10.0)
# async def auto_send(channel: discord.TextChannel):
#     await channel.send("Test Message")


# # Run Bot
# bot.run(token, log_handler=handler, log_level=logging.DEBUG)

