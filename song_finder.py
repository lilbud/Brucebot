"""song_finder gets info in inputted song."""

import re

from discord.ext import commands
from fuzzywuzzy import process

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, main_url


def song_name_fix(song: str) -> str:
    """Fix some possible incorrect song inputs, and also expands abbreviations."""
    if re.search("btr", song):
        return re.sub("btr", "born to run", song)
    elif re.search("rosie", song):  # noqa: RET505
        return re.sub("rosie", "rosalita", song)

    return song


@bot.command(name="song")
async def song_finder(ctx: commands.Context, *, args: str = "") -> None:
    """Get info on inputted song."""
    if ctx.author.id == 172307315549143040:
        await ctx.send("https://www.youtube.com/watch?v=i9AT3jjAP0Y")

    args = (
        args.replace("’", "''").replace("‘", "''").replace("”", '"').replace("‟", '"')  # noqa: RUF001
    )

    if len(args) > 1:
        song_name = song_name_fix(args)

        cur.execute("""SELECT song_name FROM SONGS""")

        songs = cur.fetchall()

        result = process.extractOne(song_name, songs)[0]

        cur.execute(
            """SELECT * FROM SONGS WHERE song_name = %s""",
            (result[0],),
        )

        s = cur.fetchone()

        if s:
            embed = create_embed(s[2], f"[Brucebase Song Page]({main_url}{s[1]})", ctx)

            embed.add_field(
                name="",
                value=f"[Lyrics]({main_url}{s[1].replace('/song:', '/lyrics:')})",
                inline=False,
            )

            if s[5] != "" and int(s[5]) > 0:
                first = re.search(r"\d{4}-\d{2}-\d{2}\w?", s[3])[0]
                last = re.search(r"\d{4}-\d{2}-\d{2}\w?", s[4])[0]

                embed.add_field(name="Performances:", value=s[5], inline=True)
                embed.add_field(
                    name="First Played:",
                    value=f"[{first}]({main_url}{s[3]})",
                    inline=True,
                )
                embed.add_field(
                    name="Last Played:",
                    value=f"[{last}]({main_url}{s[4]})",
                    inline=True,
                )
                embed.add_field(name="Show Opener:", value=s[6], inline=True)
                embed.add_field(name="Show Closer:", value=s[7], inline=True)
                embed.add_field(name="Frequency:", value=f"{s[8]}%", inline=True)
            else:
                embed.add_field(name="Performances:", value="0", inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"\nNo Results Found For: {args}")
    else:
        await ctx.send(error_message("song"))
