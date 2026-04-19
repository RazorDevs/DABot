# HELP OP COMMAND

#@slash_command(name="help", description="List and description of all commands.")
@app.load
@discohook.command.slash(name="help", description="List and description of all commands.")
async def help(i: discohook.Interaction):
    embed = discohook.Embed(title="Help", description="Here's the list of all the bots' commands.")

    if is_admin:
        embed.add_field(name="/purge", value="Removes a max of 10 messages.", inline=False)

    embed.add_field(name="/roll", value="Roll customable dices.", inline=False)
    embed.add_field(name="/faq", value="Shows our FAQ.", inline=False)
    await i.response.send(embed=embed)
