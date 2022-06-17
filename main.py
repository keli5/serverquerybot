from mcstatus import JavaServer
import discord
from discord.ext import tasks
import json

client = discord.Client()
config = json.load(open('config.json'))
last_players = 0


@tasks.loop(seconds=20)
async def query_players():
    global last_players
    server = JavaServer(config["server_ip"], config["server_port"])
    players = server.status().players.online
    pluralized = "players" if players != 1 else "player"
    if players != last_players:
        await client.change_presence(
            activity=discord.Game(
                name=f"with {f'{str(players)} {pluralized}' if players>0 else 'nobody :('}"  # noqa: E501
            )
        )
        last_players = players


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    query_players.start()


@client.event
async def on_message(message):
    description = ""
    if message.content.startswith("o!l") or message.content == client.user.mention:  # noqa: E501
        embed = discord.Embed()
        server = JavaServer(config["server_ip"], config["server_port"])
        players = server.status().players.online

        embed.title = str(players) + " players online"
        if players == 0:
            embed.color = discord.Color.red()
        else:
            embed.color = discord.Color.blue()
            for name in server.query().players.names:
                description += "- " + name + "\n"

        embed.description = description or ""
        return await message.channel.send(embed=embed)

client.run(config["token"])
