"""import_stuff all of the import statements needed for the bot."""

import datetime
import os
import urllib.parse as urlparse

import discord
import psycopg
import psycopg2
from discord.ext import commands
from zoneinfo import ZoneInfo

months = [
    "_None",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# from https://gist.github.com/rogerallen/1583593?permalink_comment_id=3699885#gistcomment-3699885
states_and_provinces_abbrev = {
    "AL": "Alabama",
    "AB": "Alberta",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "BC": "British Columbia",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NB": "New Brunswick",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "ON": "Ontario",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "QC": "Quebec",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    "DC": "District of Columbia",
}

albums = {
    "Greetings From Asbury Park, N.J.": ["greetings"],
    "The Wild, The Innocent & The E Street Shuffle": ["wiess"],
    "Born To Run": ["btr"],
    "The River": ["theriver"],
    "Born In The U.S.A.": ["bitusa", " usa"],
    "Live 1975-85": ["7585", ""],
    "Tunnel Of Love": ["tol"],
    "Human Touch": ["ht"],
    "Lucky Town": ["lt"],
    "Greatest Hits": ["greatesthits", ""],
    "The Ghost Of Tom Joad": ["gotj"],
    "Live In New York City": ["livenyc", ""],
    "The Rising": ["therising"],
    "We Shall Overcome": ["seeger", "sessions"],
    "Working On A Dream": ["woad"],
    "Wrecking Ball": ["wb", "wreckingball"],
    "High Hopes": ["hh", "highhopes"],
    "Western Stars": ["ws", "westernstars"],
    "Letter To You": ["lty", "lettertoyou"],
    "Only The Strong Survive": ["otss"],
    "The Promise": ["thepromise"],
    "The Ties That Bind": ["tttb"],
    "The Legendary 1979 No Nukes Concerts": ["nonukes", ""],
}

current_date = datetime.datetime.now(ZoneInfo("US/Eastern"))

main_url = "http://brucebase.wikidot.com"

url = urlparse.urlparse(os.environ["DATABASE_URL"])
DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


def date_checker(date: str) -> bool:
    """Verify dates entered to the setlist finder."""
    if date is not None:
        try:
            return datetime.date.fromisoformat(date)
        except ValueError:
            return False
    else:
        return False


def date_in_db(date: str) -> bool:
    """Check database for given date."""
    if date_checker(date):
        cur.execute(
            """SELECT EXISTS(SELECT 1 FROM EVENTS WHERE event_date LIKE %s)""",
            (date,),
        )

        check = cur.fetchone()

        if check:
            return True

    return False


def location_name_get(location_url: str, show: str) -> str:
    """Get venue info for a given venue_url."""
    cur.execute(
        """SELECT venue_name, venue_city, venue_state, venue_country
            FROM VENUES WHERE venue_url = %s""",
        (location_url,),
    )

    location = cur.fetchone()

    if location:
        if show != "" and show is not None:
            return f"{', '.join(list(filter(None, location[0:])))} ({show})"

        return f"{', '.join(list(filter(None, location[0:])))}"

    return ""
