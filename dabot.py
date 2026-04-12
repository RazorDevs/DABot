import asyncio
import datetime
import os
import random
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from interactions import AutoShardedClient, Intents, listen
from interactions import Embed, FlatUIColors
from interactions import OptionType, slash_option
from interactions import Task, IntervalTrigger
from interactions import check
from interactions import slash_command, SlashContext, BaseContext
from playwright.async_api import async_playwright, BrowserContext

load_dotenv(dotenv_path='./.env')

# Initialize Bot and denote the Command Prefix
bot = AutoShardedClient(intents=Intents.DEFAULT)

headers = {'Accept': 'application/json', 'x-api-key': os.getenv('CURSEFORGE_TOKEN')}

# Event when Bot Successfully Connects
@listen()
async def on_ready():
    print(f'{bot.user} succesfully logged in!')
    downloadFetch.start()

# Looping task every tot minutes for Mod Downloads Update
@Task.create(IntervalTrigger(minutes=30))
async def downloadFetch():
    async with async_playwright() as pw:
        browser = await pw.firefox.launch(headless=True)
        ctx = await browser.new_context()
        async with asyncio.TaskGroup() as tg:
            tg.create_task(update_mod_downloads(ctx, "deep-aether", "Deep Aether", 852465, int(os.getenv('DEEP_AETHER_CHANNEL'))))
            tg.create_task(update_mod_downloads(ctx, "aeroblender", "Aeroblender", 879879, int(os.getenv('AEROBLENDER_CHANNEL'))))
            tg.create_task(update_mod_downloads(ctx, "ascended-quark", "Ascended Quark", 971104, int(os.getenv('ASCENDED_QUARK_CHANNEL'))))

async def update_mod_downloads(ctx, modid, name, pid, channel_id):
    CFENDPOINT = f"https://api.curseforge.com/v1/mods/{pid}"
    MENDPOINT = f"https://api.modrinth.com/v2/project/{modid}"

    element1 = int(requests.get(CFENDPOINT, headers=headers).json()['data']['downloadCount'])
    element2 = int(requests.get(MENDPOINT).json()['downloads'])
    ch = bot.get_channel(channel_id)

    result = element1 + element2
    await ch.edit(name=f"{name}:  {result}")

# Wrong command Event

@listen()
async def on_command_error(ctx, error):
    await ctx.send("Invalid command.")
    print("Invalid Command called.")

# Checks if user is an admin

async def is_admin(ctx: BaseContext):
    return ctx.author.guild_permissions.ADMINISTRATOR

command_list = ["help", "purge", "roll", "faq", "reviews"]

for f in command_list:
    try:
        exec(compile(open(f"./commands/{f}.py", "rb").read(), f"./commands/{f}.py", 'exec'))
    except:
        print(f"There was an error with the {f} command file.")

bot.start(os.getenv('TOKEN'))
