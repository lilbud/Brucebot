"""Main function for this bot."""

import os

from discord.ext.commands import Context

from album_find import album_finder
from bootleg import bootleg_find
from bot_info import bot_help, bot_info
from get_cover import get_cover
from import_stuff import GUILD_ID, OWNER_USERID, bot, commands, discord
from jungleland import jungleland_art, jungleland_torrent
from location_finder import city_finder, country_finder, state_finder
from on_this_day import on_this_day
from relation_find import relation_finder
from setlist_finder import setlist_finder
from song_finder import song_finder
from tour_finder import tour_stats


@bot.event
async def on_ready() -> None:
    """Message to send in log if online and ready."""
    print(f"Bot online and logged in as {bot.user}")


@bot.command()
async def sync(ctx: Context) -> None:
    """Sync command."""
    print("sync command")
    if ctx.author.id == OWNER_USERID:
        await bot.tree.copy_global_to(guild=GUILD_ID)
        await bot.tree.sync(guild=GUILD_ID)
        await ctx.send("Command tree synced.")
    else:
        await ctx.send("You must be the owner to use this command!")


my_secret = os.environ["TOKEN"]
bot.run(my_secret)
