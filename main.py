import discord
import json
from discord import app_commands

from utils import exchange, getResult, getUsers, setClues, getClues, getHelp


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
    # if message.content == 'test':
    #     setClues("111", "222")
    #     await message.channel.send('123')

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
async def first_command(interaction):
    await interaction.response.send_message(getHelp())


@tree.command(
    name = "clue",
    description = "設定線索, 格式: 玩家名稱, 線索",
    guild=discord.Object(id=1063079372568924250)
)
async def first_command(interaction, clue: str):
    setClues(clue)
    clues = getClues()
    await interaction.response.send_message(clues)

@tree.command(
    name = "clues",
    description = "顯示目前的線索清單",
    guild=discord.Object(id=1063079372568924250)
)
async def first_command(interaction):
    clues = getClues()
    await interaction.response.send_message(clues)

@tree.command(
    name = "users",
    description = "顯示玩家清單",
    guild=discord.Object(id=1063079372568924250)
)
async def first_command(interaction):
    users = getUsers()
    await interaction.response.send_message(users)

@tree.command(
    name = "result",
    description = "顯示計算結果",
    guild=discord.Object(id=1063079372568924250)
)
async def first_command(interaction):
    result = getResult()
    await interaction.response.send_message(result)


client.run(data['token'])