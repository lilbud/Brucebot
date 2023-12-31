import re
from import_stuff import bot, cur, main_url
from create_embed import create_embed
from error_message import error_message


def tour_name_fix(tour):
    # btr, river, bitusa, tol, other band, human touch, lucky town
    if tour is not None:
        if tour == "btr":
            return "born to run"
        elif tour == "river":
            return "the river tour"
        elif tour == "bitusa":
            return "born in the u.s.a. tour"
        elif re.search("(tunnel|tol)", tour, re.IGNORECASE):
            return "tunnel of love"
        elif re.search("usa", tour, re.IGNORECASE):
            return tour.replace("usa", "u.s.a.")
        elif re.search("(92|93)", tour, re.IGNORECASE):
            return "world tour 1992-93"
        elif re.search("(16|2016)", tour, re.IGNORECASE):
            return "the river tour '16"
        else:
            return tour


@bot.command(aliases=["tour"])
async def tour_stats(ctx, *tour):
    # id, url, name, first_show_url, last_show_url, num_shows, num_songs

    if len(" ".join(tour)) > 1:
        tour_name = tour_name_fix(" ".join(tour))
        stats = ""

        if cur.execute(
            f"""SELECT * FROM TOURS WHERE tour_name ILIKE '{tour_name.replace("'", "''")}'"""
        ).fetchall():
            stats = cur.execute(
                f"""SELECT * FROM TOURS WHERE tour_name ILIKE '{tour_name.replace("'", "''")}'"""
            ).fetchall()[0]
        elif cur.execute(
            f"""SELECT * FROM TOURS WHERE tour_name ILIKE '%{tour_name.replace("'", "''")}%'"""
        ).fetchall():
            stats = cur.execute(
                f"""SELECT * FROM TOURS WHERE tour_name ILIKE '%{tour_name.replace("'", "''")}%'"""
            ).fetchall()[0]

        if stats != "":
            first_show = cur.execute(
                f"""SELECT event_date FROM EVENTS WHERE tour LIKE '{stats[2].replace("'", "''")}' AND event_url LIKE '{str(stats[3])}' AND event_url LIKE '/gig:%'"""
            ).fetchall()[0]
            last_show = cur.execute(
                f"""SELECT event_date FROM EVENTS WHERE tour LIKE '{stats[2].replace("'", "''")}' AND event_url LIKE '{str(stats[4])}' AND event_url LIKE '/gig:%'"""
            ).fetchall()[0]

            embed = create_embed(
                f"Tour: {stats[2]}",
                f"[Tour Stats]({main_url}{stats[1]}) | [Tour Songs]({main_url}{stats[1].replace('shows', 'songs')})",
                ctx,
            )

            # first show, last show, num shows, num songs
            embed.add_field(name="Number of Shows:", value=f"{stats[5]}", inline=False)
            embed.add_field(
                name="First Show:",
                value=f"[{first_show[0]}]({main_url}{str(stats[3])})",
                inline=False,
            )
            embed.add_field(
                name="Last Show:",
                value=f"[{last_show[0]}]({main_url}{str(stats[4])})",
                inline=False,
            )
            embed.add_field(name="Number of Songs:", value=f"{stats[6]}", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(error_message("tour"))
    else:
        await ctx.send(error_message("tour"))
