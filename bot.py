from discord.ext import commands
import discord
import json
import websockets
import asyncio
import os
import csv

# Discord bot prefix


def get_server_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]


# Discord part
TOKEN = 'MTA0NTc3NDU1ODU1NDIzOTExNg.G1l8r6.ayE_uliYHJ1k3UPv-Pv3Bl-6B85-J02yifJnWw'
client = commands.Bot(command_prefix=get_server_prefix,
                      intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    os.startfile(rf"D:\codus\koomer.py")
    await(main())


@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = "!"

    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)


# prefix changer

@client.command()
async def setprefix(ctx, *, newprefix: str):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix[str(ctx.guild.id)] = newprefix

    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

# New link add


@client.command()
async def newlink(ctx, *, message):
    if ctx.author.bot:
        return
    with open("links.txt", "a") as file:
        file.write(f"https://www.reddit.com/r/{message}/new/\n")
    await ctx.send("Link is saved!")


@client.command()
async def deletelink(ctx, word: str):
    with open('links.txt', 'r') as file:
        lines = file.readlines()
    with open('links.txt', 'w') as file:
        for line in lines:
            if word not in line:
                file.write(line)
    await ctx.send(f'Link was deleted')


@client.event
async def redditpost(found):
    print(found)
    general_channel = discord.utils.get(
        client.get_all_channels(), name='general')
    if found != "":
        await general_channel.send(f"https://www.reddit.com{found}")


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)
        await redditpost(message)
        await websocket.close()


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


client.run(TOKEN)
