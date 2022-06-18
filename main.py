from mcstatus import JavaServer
import discord
from discord.ext import tasks, commands
import json
from cogs.server import Server

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("o!"),
)
config = json.load(open('config.json'))
last_players = -1  # -1 so no players is still a change
cogs_to_load = ["server", "jishaku"]


@tasks.loop(seconds=20)
async def query_players():
    global last_players
    server = JavaServer(config["server_ip"], config["server_port"])
    players = server.status().players.online
    pluralized = "players" if players != 1 else "player"
    if players != last_players:
        await bot.change_presence(
            activity=discord.Game(
                name=f"with {f'{str(players)} {pluralized}' if players>0 else 'nobody :('}"
            )
        )
        last_players = players


@bot.event
async def on_message(msg):
    if msg.author.bot:
        return False
    if msg.content == bot.user.mention:
        return await Server.list("", msg.channel)  # this should be self and a ctx, but I don't know how to do that
    await bot.process_commands(msg)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    query_players.start()

if __name__ == "__main__":
    for cog in cogs_to_load:
        bot.load_extension(f"cogs.{cog}")


bot.run(config["token"])
