import asyncio
import datetime
import os
import random
import requests
import discohook

from workers import WorkerEntrypoint, Response

import commands.help
import commands.faq

# Checks if user is an admin
async def is_admin(ctx: discohook.Interaction):
    return ctx.author.permissions.administrator

class Bot(WorkerEntrypoint):
    async def fetch(self, req, env):
        app = discohook.Client(
            application_id=env.APP_ID,
            public_key=env.KEY,
            token=env.TOKEN,
            password=env.APP_PSW
        )

        # Wrong command Event
        @app.on_interaction_error()
        async def on_command_error(i: discohook.Interaction, error: Exception):
            user_response = "Some error occurred!"
            if i.responded:
                await i.response.followup(user_response, ephemeral=True)
            else:
                await i.response.send(user_response, ephemeral=True)
            print(f"Command error occurred. {error}")

        app.add_commands(help, faq)

        return await app.handle(request)

    async def scheduled(self, event, env):
        headers = {'Accept': 'application/json', 'x-api-key': env.CURSEFORGE_TOKEN}

        async def update_downloads(modid, name, pid, channel_id):
            CFENDPOINT = f"https://api.curseforge.com/v1/mods/{pid}"
            MENDPOINT = f"https://api.modrinth.com/v2/project/{modid}"

            el1 = int(requests.get(CFENDPOINT, headers=headers).json()['data']['downloadCount'])
            el2 = int(requests.get(MENDPOINT).json()['downloads'])
            ch = bot.get_channel(channel_id)

            result = el1 + el2
            discord_api_url = f"https://discord.com/api/v10/channels/{channel_id}"
            discord_headers = {
                "Authorization": f"Bot {env.TOKEN}",
                "Content-Type": "application/json"
            }
            discord_json = {"name": f"{name}:  {result}"}

            response = requests.patch(discord_api_url, headers=discord_headers, json=discord_json)
            if response.status_code == 200:
                print(f"Successfully updated {name} to {result}")
            else:
                print(f"Failed to update {name}. Discord replied: {response.text}")

        update_mod_downloads("deep-aether", "Deep Aether", 852465, int(env.DEEP_AETHER_CHANNEL))
        update_mod_downloads("aeroblender", "Aeroblender", 879879, int(env.AEROBLENDER_CHANNEL))
        update_mod_downloads("ascended-quark", "Ascended Quark", 971104, int(env.ASCENDED_QUARK_CHANNEL))
