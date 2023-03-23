import discord
import json
from discord import app_commands

from utils import exchange, getResult


with open('items.json', "r", encoding = "utf8") as file:
    data = json.load(file)
print(data["token"])

#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1063079372568924250))
    print('目前登入身份：', client.user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'ping':
        await message.channel.send('pong')
    if message.content == 'exchange':
        exchange()
        await message.channel.send('計算完成')
    if message.content == 'test':
        result = getResult()
        await message.channel.send(result)

@tree.command(
    name = "exchange",
    description = "輸入線索",
    guild=discord.Object(id=1063079372568924250)
)
async def first_command(interaction, arg: str):
    exchange()
    await interaction.response.send_message(f"計算完成")


@tree.command(
    name = "help",
    description = "各功能說明",
    guild=discord.Object(id=1063079372568924250)
)
async def first_command(interaction, arg: str):
    await interaction.response.send_message("TODO")


@tree.command(
    name = "clues",
    description = "各功能說明",
    guild=discord.Object(id=1063079372568924250)
)
async def first_command(interaction, arg: str):
    await interaction.response.send_message("TODO")

@tree.command(
    name = "result",
    description = "回傳計算結果",
    guild=discord.Object(id=1063079372568924250)
)
async def first_command(interaction):
    result = getResult()
    await interaction.response.send_message(result)


client.run(data['token'])