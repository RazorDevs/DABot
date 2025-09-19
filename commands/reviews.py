# TODO: Reviews Command

@slash_command(name='review', description="Leave an anonymous review for the mod!")
async def sendReview(ctx: SlashContext, text):
    embed = Embed(color = FlatUICOlors.CARROT)
    ch = bot.get_channel(int(os.getenv('REVIEWS_CHANNEL'))) # Reviews Channel
    embed.add_field(name="Review", value=text, inline=False)
    await ctx.send("Review sent!", ephemeral=True)
    await ch.send(embed=embed)
