import discord
from discord.ext import commands
from discord.ext.tasks import loop
import asyncio
import sqlite3
import time
from discord.ext.commands import has_permissions,RoleConverter, MemberConverter
from datetime import datetime, timezone, timedelta

client = discord.Client()
client = commands.Bot(".")

@client.event
async def on_ready():
    print('Bot is online')

@client.event
async def on_message(message):

    await client.process_commands(message)

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


#command which send link to your DM ..(works only in #link to lobby **F5**)
@client.command()
async def link_A(ctx):
    user = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="GroupA")
    for i in user.roles:
        if i.name == role.name:
            conn = sqlite3.connect('link.db')
            result = conn.execute("SELECT link,time FROM links WHERE grou = :group", {"group":"A"})
            em = discord.Embed(title="Database")
            if result.fetchone() is not None and result is not None:
                for row in result.fetchone():
                        em.add_field(name="Details", value=f"{row}")
            else:
                em.add_field(name="link", value="MATCH HAS STARTED OR ROOM HAS NOT BEEN CREATED YET")
            msg = await ctx.author.send(embed=em)
            conn.close()
            return
    print(user.roles)
    await ctx.author.send("You are not the part of GroupA")


@client.command(name="link_in_A")
async def link_in_A(ctx, time, *, link):
    user = ctx.author

    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    seconds = 0
    if link is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("days"):
        seconds += int(time[:-4]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    elif time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send reminder_help for more information.')
    elif seconds < 1:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 1 second.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        print("done")
        x = utc_to_local(ctx.message.created_at)+timedelta(seconds=seconds)
        x= x.strftime("%B %d, %Y %I:%M%p")
        conn = sqlite3.connect('link.db')
        cursor = conn.execute('''CREATE TABLE IF NOT EXISTS links(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT NOT NULL,
        time timestamp NOT NULL,
        grou TEXT NOT NULL
        )''')
        print ("Opened database successfully")
        conn.execute("INSERT INTO links(link, time, grou) VALUES (:teamname, :message, :grou)", {"teamname": link, "message": x, "grou":"A"})
        conn.commit()

        await asyncio.sleep(seconds+120)
        print("DELETE")
        conn.execute("DELETE FROM links where link = :link", {"link":link})
        conn.commit()
        conn.close()

@client.command()
async def delete_link(ctx, link):
    conn = sqlite3.connect('link.db')
    conn.execute("DELETE FROM links where link = :link", {"link":link})
    conn.commit()
    conn.close()
#purge command
@client.command()
async def link_B(ctx):
    user = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="GroupB")
    for i in user.roles:
        if i.name == role.name:
            conn = sqlite3.connect('link.db')
            result = conn.execute("SELECT link,time FROM links WHERE grou = :group", {"group":"B"})
            em = discord.Embed(title="Database")
            if result.fetchone() is not None and result is not None:
                for row in result.fetchone():
                    em.add_field(name="link", value=f"{row}")
            else:
                em.add_field(name="link", value="MATCH HAS STARTED")
            msg = await ctx.author.send(embed=em)
            conn.close()
            return
    print(user.roles)
    await ctx.author.send("You are not the part of GroupB")
@client.command(name="link_in_B")
async def link_in_B(ctx, time, *, link):
    user = ctx.author

    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    seconds = 0
    if link is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("days"):
        seconds += int(time[:-4]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    elif time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send reminder_help for more information.')
    elif seconds < 1:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 1 second.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        print("done")
        x = utc_to_local(ctx.message.created_at)+timedelta(seconds=seconds)
        x= x.strftime("%B %d, %Y %I:%M%p")
        conn = sqlite3.connect('link.db')
        cursor = conn.execute('''CREATE TABLE IF NOT EXISTS links(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT NOT NULL,
        time timestamp NOT NULL,
        grou TEXT NOT NULL
        )''')
        print ("Opened database successfully")
        conn.execute("INSERT INTO links(link, time, grou) VALUES (:teamname, :message, :grou)", {"teamname": link, "message": x, "grou":"B"})
        conn.commit()

        await asyncio.sleep(seconds+120)
        print("DELETE")
        conn.execute("DELETE FROM links where link = :link", {"link":link})
        conn.commit()

        conn.close()



client.run("NzM2NDkyMDI3MzgxOTQwMjY0.Xxvlpg.RjLx3y6csJbeCg8BBvdBs3ExFXs")
