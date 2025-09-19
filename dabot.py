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

load_dotenv()

# Initialize Bot and denote the Command Prefix
bot = AutoShardedClient(intents=Intents.DEFAULT)

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

# HELP OP COMMAND

@slash_command(name="help", description="List and description of all commands.")
async def help(ctx: SlashContext):
    embed = Embed(title="Help", description="Here's the list of all the bots' commands.")

    if is_admin:
        embed.add_field(name="/purge", value="Removes a max of 10 messages.", inline=False)

    embed.add_field(name="/roll", value="Roll customable dices.", inline=False)
    embed.add_field(name="/faq", value="Shows our FAQ.", inline=False)
    await ctx.send(embed=embed)

# Checks if user is an admin

async def is_admin(ctx: BaseContext):
    return ctx.author.guild_permissions.ADMINISTRATOR


# Rolls a number of dices.

@slash_command(name='roll', description='Rolls a max of 5 dices, with a max of 20 faces.')
@slash_option(
    	    name="dices",
	    description="Number of Dices",
	    opt_type=OptionType.INTEGER,
	    required=False
	)
@slash_option(
	    name="faces",
	    description="Number of Faces",
	    opt_type=OptionType.INTEGER,
	    required=False
	)
async def roll(ctx: SlashContext, dices=1, faces=6):
    if int(dices) > 5 or int(faces) > 20:
        print("Roll request exceeds limit.") 
        await ctx.send("Roll request exceeds limit.")
    else:
        rolls = [] 
        for x in range(int(dices)):
            rolls.append(random.randint(1, int(faces))) 
        print(f'Rolled: {rolls};') 
        await ctx.send(str(rolls))

# Clean command for a maximum of 10 messages.

@slash_command(name='purge', description="Removes a max of 10 messages.")
@slash_option(
	    name="num",
	    description="Number of messages",
	    opt_type=OptionType.INTEGER,
	    required=False
	)
@check(is_admin)
async def purge(ctx: SlashContext, num=1):
    if num <= 10:
        num += 1
        await ctx.channel.purge(deletion_limit=num)
        num -= 1
        await ctx.send(f"Removed {num} messages.")
    else:
        await ctx.send("That's too many!", ephemeral=True)

# FAQ Command to answer questions. Currently hardcoded
# TODO: Dynamically retrieve the Q&A (No TXT file)

@slash_command(name='faq', description="Prints the FAQ of Deep Aether.")
async def faq(ctx: SlashContext):
    embed = Embed(title="FAQ", color = FlatUIColors.CARROT)

    embed.add_field(name="Q: Do you plan on backporting to other versions?", 
        value="A: No we don't. The Aether Mod only plans releases from 1.19.2 and onwards, meaning this addon cannot reach versions that are prior to that.", inline=False)
    embed.add_field(name="Q: Where can I get Sterling Aerclouds? I can't find any!",
        value="A: Sterling Aerclouds are found above Y = 200. If you're playing with a low render distance it might be harder to spot the clusters, *but they're there*!",
        inline=False)
    embed.add_field(name="Q: I'm having trouble finding info about the mod, where can I look for it?",
        value="A: Unfortunately there's currently no good source of information other than asking us directly. We're working on a wiki hosted on the official Aether one, but we're in desperate need of help!", inline=False)
    embed.add_field(name="Q: Do you plan on adding cross-compatibility with other mods and Aether addons?", 
        value="A: Yes, we have already done that with many of the popular addons: Aether Lost Content, Aether Redux, and more!", inline=False)
    embed.add_field(name="Q: I am interested in joining your team to help with the development of the mod! How can I do so?",
        value=f"A: We are always open to accepting new members, especially testers, and developers. See {bot.get_channel(1115999673673592832).mention}.", inline=False)

    await ctx.send(embed=embed)

# TODO: Reviews Command

@slash_command(name='review', description="Leave an anonymous review for the mod!")
async def sendReview(ctx: SlashContext, text):
    embed = Embed(color = FlatUICOlors.CARROT)
    ch = bot.get_channel(int(os.getenv('REVIEWS_CHANNEL'))) # Reviews Channel
    embed.add_field(name="Review", value=text, inline=False)
    await ctx.send("Review sent!", ephemeral=True)
    await ch.send(embed=embed)


bot.start(os.getenv('TOKEN'))
