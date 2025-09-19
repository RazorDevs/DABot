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
