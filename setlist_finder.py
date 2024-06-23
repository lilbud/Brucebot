"""setlist_finder gets setlist based on inputted date."""

from discord.ext import commands

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, date_in_db, location_name_get, main_url


@bot.hybrid_command(name="setlist", aliases=["sl", "show"])
async def setlist_finder(ctx: commands.Context, date: str = "") -> None:  # noqa: C901, PLR0912, PLR0915
    """Get setlist based on input date."""
    if date == "":
        cur.execute(
            """SELECT event_date FROM EVENTS WHERE setlist != ''
            ORDER BY event_id DESC LIMIT 1""",
        )

        date = cur.fetchone()[0]
        print(date)

    if date_in_db(date):
        embed = create_embed(f"Brucebase Results For: {date}", "", ctx)
        cur.execute(
            """SELECT * FROM EVENTS WHERE event_date = %s""",
            (date,),
        )

        get_events = cur.fetchall()

        invalid_sets = []

        cur.execute(
            """SELECT set_type FROM (SELECT DISTINCT ON (set_type) * FROM SETLISTS WHERE
            set_type SIMILAR TO '%(Soundcheck|Rehearsal)%') p""",
        )

        sets = cur.fetchall()

        for i in sets:
            invalid_sets.append(i[0])  # noqa: PERF401

        if get_events:
            for r in get_events:
                tags = []

                if r[7]:
                    tags.append("Bootleg")

                if r[8]:
                    tags.append("Official Release")

                if not r[7] and not r[8]:
                    tags.append("Uncirculating")

                location = location_name_get(r[3], r[4])
                releases = f"**Releases:** {', '.join(tags)}"

                embed.add_field(
                    name="",
                    value=f"[{r[1]} - {location}]({main_url}{r[2]})\n{releases}",
                    inline=False,
                )
                embed.set_footer(text=r[5])

                cur.execute(
                    """SELECT EXISTS(SELECT 1 FROM SETLISTS WHERE event_url = %s)""",
                    (r[2],),
                )

                has_setlist = cur.fetchone()

                if has_setlist[0] != 0:
                    location = setlist = indicator = ""
                    cur.execute(
                        """SELECT set_type FROM (SELECT DISTINCT ON (set_type) * FROM
                        SETLISTS WHERE event_url = %s) p ORDER BY
                        setlist_song_id ASC""",
                        (r[2],),
                    )
                    set_types = cur.fetchall()

                    for s in set_types:
                        set_l = []

                        cur.execute(
                            """SELECT song_name, song_url, segue FROM SETLISTS
                            WHERE event_url = %s AND set_type =
                            %s ORDER BY setlist_song_id ASC""",
                            (r[2], s[0].replace("'", "''")),
                        )

                        set_songs = cur.fetchall()

                        for song in set_songs:
                            indicator = note = segue = ""
                            cur.execute(
                                """SELECT EXISTS(SELECT 1 FROM SONGS WHERE song_url = %s
                                AND first_played = %s)""",
                                (song[1], r[2]),
                            )
                            premiere = cur.fetchone()

                            cur.execute(
                                """SELECT MIN(event_url) FROM EVENTS WHERE setlist
                                LIKE %s AND tour LIKE %s""",
                                (
                                    "%" + song[0].replace("'", "''") + "%",
                                    r[5].replace("'", "''"),
                                ),
                            )

                            bustout = cur.fetchone()

                            """indicator is [1] or [2]"""
                            if s[0] not in invalid_sets:
                                if premiere[0] != 0:
                                    indicator = " **[1]**"

                                if bustout[0] == r[2]:
                                    indicator = " **[2]**"

                            if song[2]:
                                segue = " >"

                            set_l.append(f"{song[0]}{indicator}{segue}")

                        setlist = ", ".join(set_l).replace(">,", ">")

                        if not r[7] and not r[8]:
                            note = "(Setlist May Be Incomplete)"

                        embed.add_field(
                            name=f"{s[0]} {note}:",
                            value=setlist,
                            inline=False,
                        )
                else:  # end "if has_setlist"
                    embed.add_field(
                        name="",
                        value=error_message("no-setlist"),
                        inline=False,
                    )

            embed.add_field(
                name="",
                value="**[1]** - First Known Performance\n**[2]** - Tour Debut",
            )
        else:  # end "if get_events"
            embed.add_field(name="", value=error_message("show"), inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{error_message('date')} - {date}")
