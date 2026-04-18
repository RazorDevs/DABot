import asyncio
import datetime
import os
import random
import requests
import discohook

from workers import env
from dotenv import load_dotenv

load_dotenv()

app = discohook.Client(
    application_id=env.APP_ID,
    public_key=env.KEY,
    token=env.TOKEN,
    password=env.APP_PSW
)

headers = {'Accept': 'application/json', 'x-api-key': env.CURSEFORGE_TOKEN}

# Event when Bot Successfully Connects
async def on_ready():
    print(f'{bot.user} succesfully logged in!')
    downloadFetch.start()

# Looping task every few minutes for Mod Downloads Update
async def downloadFetch():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(update_mod_downloads("deep-aether", "Deep Aether", 852465, int(env.DEEP_AETHER_CHANNEL)))
        tg.create_task(update_mod_downloads("aeroblender", "Aeroblender", 879879, int(env.AEROBLENDER_CHANNEL)))
        tg.create_task(update_mod_downloads("ascended-quark", "Ascended Quark", 971104, int(env.ASCENDED_QUARK_CHANNEL)))

async def update_mod_downloads(modid, name, pid, channel_id):
    CFENDPOINT = f"https://api.curseforge.com/v1/mods/{pid}"
    MENDPOINT = f"https://api.modrinth.com/v2/project/{modid}"

    element1 = int(requests.get(CFENDPOINT, headers=headers).json()['data']['downloadCount'])
    element2 = int(requests.get(MENDPOINT).json()['downloads'])
    ch = bot.get_channel(channel_id)

    result = element1 + element2
    await ch.edit(name=f"{name}:  {result}")

# Wrong command Event
@app.on_interaction_error()
async def on_command_error(i: discohook.Interaction, error: Exception):
    user_response = "Some error occurred!"
    if i.responded:
        await i.response.followup(user_response, ephemeral=True)
    else:
        await i.response.send(user_response, ephemeral=True)
    print(f"Command error occurred. {error}")

# Checks if user is an admin
async def is_admin(ctx: BaseContext):
    return ctx.author.guild_permissions.ADMINISTRATOR

command_list = ["help", "faq"]

for f in command_list:
    try:
        exec(compile(open(f"./commands/{f}.py", "rb").read(), f"./commands/{f}.py", 'exec'))
    except:
        print(f"There was an error with the {f} command file.")
