import datetime
import os
import random

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from interactions import AutoShardedClient, Intents, listen
from interactions import Embed, FlatUIColors
from interactions import OptionType, slash_option
from interactions import Task, IntervalTrigger
from interactions import check
from interactions import slash_command, SlashContext, BaseContext
from playwright.async_api import async_playwright, Playwright, Locator


# Event when Bot Successfully Connects
@listen()
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

    downloadFetch.start()

# Looping task every tot minutes for Mod Downloads Update
@Task.create(IntervalTrigger(minutes=15))
async def downloadFetch():
    await update_mod_downloads("deep-aether", "Deep Aether", int(os.getenv('DEEP_AETHER_CHANNEL')))
    await update_mod_downloads("aeroblender", "Aeroblender", int(os.getenv('AEROBLENDER_CHANNEL')))
    await update_mod_downloads("ascended-quark", "Ascended Quark", int(os.getenv('ASCENDED_QUARK_CHANNEL')))

    with open("log.txt", 'w') as logfile:
        logfile.write(str(datetime.datetime.now()))


async def update_mod_downloads(modid, name, channel_id):
    async with async_playwright() as pw:
        browser = await pw.firefox.launch()
        CFURL = f"https://www.curseforge.com/minecraft/mc-mods/{modid}"
        MRURL = f"https://modrinth.com/mod/{modid}"

        page = await browser.new_page()
        await page.goto(CFURL)
        element1 = await page.locator(".detail-downloads").all_text_contents()

        await page.goto(MRURL)
        element2 = await page.locator(".flex .items-center .gap-2 .border-0 .border-r .border-solid .border-divider .pr-4 .font-semibold .cursor-help .v-popper--has-tooltip").all_text_contents()

        ch = bot.get_channel(channel_id)
        result = int(element1[0].replace(",","")) + 0 #int(element2.text.replace("k","00").replace(".",""))
        await ch.edit(name=f"{name}:  {result}")
        await browser.close()


# Wrong command Event

@listen()
async def on_command_error(ctx, error):
    await ctx.send("Invalid command.")
    print("Invalid Command called.")

# Checks if user is an admin

async def is_admin(ctx: BaseContext):
    return ctx.author.guild_permissions.ADMINISTRATOR


def main():
    # Initialize Bot and denote the Command Prefix
    bot = AutoShardedClient(intents=Intents.DEFAULT)

    load_dotenv(dotenv_path='./.env')
    command_list = ["help", "purge", "roll", "faq", "reviews"]

    for f in command_list:
        try:
            exec(compile(open(f"commands/{f}.py", "rb").read(), f"commands/{f}.py", 'exec'))
        except:
            print(f"There was an error with the {f} command file.")

    bot.start(os.getenv('TOKEN'))


if __name__=="__main__":
    main()
