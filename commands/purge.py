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
