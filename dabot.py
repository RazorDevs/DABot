import sys
from types import ModuleType

# --- MOCK NACL ---
def mock_nacl():
    nacl = ModuleType("nacl")
    nacl.__path__ = []  
    nacl_exceptions = ModuleType("nacl.exceptions")
    class BadSignatureError(Exception):
        pass
    nacl_exceptions.BadSignatureError = BadSignatureError
    nacl_signing = ModuleType("nacl.signing")
    class VerifyKey:
        def __init__(self, key_bytes, encoder=None):
            self.key_bytes = key_bytes
        def verify(self, message, signature):
            return message
    nacl_signing.VerifyKey = VerifyKey

    sys.modules["nacl"] = nacl
    sys.modules["nacl.exceptions"] = nacl_exceptions
    sys.modules["nacl.signing"] = nacl_signing

mock_nacl()

import os
import asgi
import discohook
import httpx
from workers import WorkerEntrypoint

# Cache the bot instance globally
bot_app = None

async def is_admin(ctx: discohook.Interaction):
    # Make sure we handle cases where the command is used in DMs (permissions might be None)
    if not ctx.author.permissions:
        return False
    return ctx.author.permissions.administrator

@discohook.command.slash(name='faq', description="Prints the FAQ of Deep Aether.")
async def faq_cmd(i: discohook.Interaction):
    embed = discohook.Embed(title="FAQ", color=0xe67e22)

    embed.add_field(name="Q: Do you plan on backporting to other versions?",
        value="A: No we don't. The Aether Mod only plans releases from 1.19.2 and onwards, meaning this addon cannot reach versions that are prior to that.", inline=Fa>
    embed.add_field(name="Q: Where can I get Sterling Aerclouds? I can't find any!",
        value="A: Sterling Aerclouds are found above Y = 200. If you're playing with a low render distance it might be harder to spot the clusters, *but they're there*>
        inline=False)
    embed.add_field(name="Q: I'm having trouble finding info about the mod, where can I look for it?",
        value="A: We finally have some info on the Wiki! Check it out at https://aether.wiki.gg/wiki/Deep_Aether.", inline=False)
    embed.add_field(name="Q: Do you plan on adding cross-compatibility with other mods and Aether addons?",
        value="A: Yes, we have already done that with many of the popular addons: Aether Lost Content, Aether Redux, and more!", inline=False)

    embed.add_field(name="Q: I am interested in joining your team to help with the development of the mod! How can I do so?",
        value="A: We are always open to accepting new members, especially testers, and developers. See <#1115999673673592832>.", inline=False)

    await i.response.send(embed=embed)

@discohook.command.slash(name="help", description="List and description of all commands.")
async def help_cmd(i: discohook.Interaction):
    embed = discohook.Embed(title="Help", description="Here's the list of all the bots' commands.")

    if await is_admin(i):
        embed.add_field(name="/purge", value="Removes a max of 10 messages.", inline=False)

    embed.add_field(name="/roll", value="Roll customable dices.", inline=False)
    embed.add_field(name="/faq", value="Shows our FAQ.", inline=False)
    await i.response.send(embed=embed)

def setup_bot(env):
    """Initializes the bot and registers commands once."""
    app = discohook.Client(
        application_id=env.APP_ID,
        public_key=env.KEY,
        token=env.TOKEN,
        password=env.APP_PSW
    )

    @app.on_interaction_error()
    async def on_command_error(i: discohook.Interaction, error: Exception):
        user_response = "Some error occurred!"
        if i.responded:
            await i.response.followup(user_response, ephemeral=True)
        else:
            await i.response.send(user_response, ephemeral=True)
        print(f"Command error occurred. {error}")

    app.add_commands(help, faq)
    return app

class Default(WorkerEntrypoint):
    async def fetch(self, req):
        global bot_app
        if bot_app is None:
            bot_app = setup_bot(self.env)
            
        return await asgi.fetch(bot_app, req, self.env)

    async def scheduled(self, event, env, ctx):
        cf_headers = {'Accept': 'application/json', 'x-api-key': env.CURSEFORGE_TOKEN}
        
        async with httpx.AsyncClient() as client:

            async def update_downloads(modid, name, pid, channel_id):
                CFENDPOINT = f"https://api.curseforge.com/v1/mods/{pid}"
                MENDPOINT = f"https://api.modrinth.com/v2/project/{modid}"

                cf_resp = await client.get(CFENDPOINT, headers=cf_headers)
                el1 = int(cf_resp.json()['data']['downloadCount'])
                
                m_resp = await client.get(MENDPOINT)
                el2 = int(m_resp.json()['downloads'])

                result = el1 + el2
                
                discord_api_url = f"https://discord.com/api/v10/channels/{channel_id}"
                discord_headers = {
                    "Authorization": f"Bot {env.TOKEN}",
                    "Content-Type": "application/json"
                }
                discord_json = {"name": f"{name}: {result}"}

                response = await client.patch(discord_api_url, headers=discord_headers, json=discord_json)
                if response.status_code == 200:
                    print(f"Successfully updated {name} to {result}")
                else:
                    print(f"Failed to update {name}. Discord replied: {response.text}")

            # Added awaits and fixed the function name call
            await update_downloads("deep-aether", "Deep Aether", 852465, int(env.DEEP_AETHER_CHANNEL))
            await update_downloads("aeroblender", "Aeroblender", 879879, int(env.AEROBLENDER_CHANNEL))
            await update_downloads("ascended-quark", "Ascended Quark", 971104, int(env.ASCENDED_QUARK_CHANNEL))
