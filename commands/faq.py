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
        value="A: We finally have some info on the Wiki! Check it out at https://aether.wiki.gg/wiki/Deep_Aether.", inline=False)
    embed.add_field(name="Q: Do you plan on adding cross-compatibility with other mods and Aether addons?",
        value="A: Yes, we have already done that with many of the popular addons: Aether Lost Content, Aether Redux, and more!", inline=False)
    embed.add_field(name="Q: I am interested in joining your team to help with the development of the mod! How can I do so?",
        value=f"A: We are always open to accepting new members, especially testers, and developers. See {bot.get_channel(1115999673673592832).mention}.", inline=False)

    await ctx.send(embed=embed)
