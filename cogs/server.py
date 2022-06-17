import discord
import json
from mcstatus import JavaServer
from discord.ext import commands

config = json.load(open('config.json'))


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def list(self, ctx):
        description = ""
        embed = discord.Embed()
        server = JavaServer(config["server_ip"], config["server_port"])
        players = server.status().players.online
        maxplayers = server.status().players.max

        embed.title = f"{str(players)}/{str(maxplayers)} players online"
        if players == 0:
            embed.color = discord.Color.red()
        else:
            embed.color = discord.Color.blue()
            for name in server.query().players.names:
                description += "- " + name + "\n"

        embed.description = description or ""
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Server(bot))
