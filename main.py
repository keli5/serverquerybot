from mcstatus import JavaServer
import discord
import json

client = discord.Client()
config = json.load(open('config.json'))


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
