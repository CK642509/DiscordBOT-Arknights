import discord
import json
from discord import app_commands

from utils import exchange, getResult, getUsers, setClues, getClues, getDetail, getHelp, formatClues


with open('config.json', "r", encoding = "utf8") as file:
    config = json.load(file)
print(config["token"])
print(config["GUILD_ID"])

# GUILD_ID=1063079372568924250
GUILD_ID = config["GUILD_ID"]
CLUE_CHANNEL_ID = config["CLUE_CHANNEL_ID"]
CHAT_CHANNEL_ID = config["CHAT_CHANNEL_ID"]
TEST_CHANNEL_ID = config["TEST_CHANNEL_ID"]

#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print('目前登入身份：', client.user)

@client.event
async def on_message(message):
    if message.author == client.user and message.content == '計算完成':
        result = getResult()
        await client.get_channel(CLUE_CHANNEL_ID).send(result)
    elif message.author == client.user:
        return
    else:
        print(message.author.id, message.author.name, message.content)
        print(message.channel.id)
        # print(message.guild.id)
        try:
            user = config["users"][str(message.author.id)]
            print(user)
        except:
            print("not exist in user list")
    
    if message.content == 'ping':
        await message.channel.send('pong')
    if message.content == 'exchange':
        exchange()
        await message.channel.send('計算完成')
    if message.content == 'test':
        print(formatClues("1112345 123"))
        print(formatClues("1112345"))
        print(formatClues("1112345   1"))
        await client.get_channel(TEST_CHANNEL_ID).send("XD")
    # 更新線索
    if message.channel.id == CLUE_CHANNEL_ID and message.author.id != 525463925194489876:
        user = config["users"][str(message.author.id)]
        clues = formatClues(message.content)
        setClues(f"{user}, {clues}")
        # clues = getClues()
        # await client.get_channel(TEST_CHANNEL_ID).send(clues)
        detail = getDetail()
        await client.get_channel(TEST_CHANNEL_ID).send(f"```{detail}```")
    # 更新線索 (小蔡)
    if message.channel.id == CLUE_CHANNEL_ID and message.author.id == 525463925194489876:
        # TODO: 整理成函數
        clue_1 = message.content.split("\n")[0]
        clue_2 = message.content.split("\n")[1]
        user_1 = clue_1.split(":")[0]
        user_2 = clue_2.split(":")[0]
        clues_1 = formatClues(clue_1.split(":")[1])
        clues_2 = formatClues(clue_2.split(":")[1])
        setClues(f"{user_1}, {clues_1}")
        setClues(f"{user_2}, {clues_2}")
        # clues = getClues()
        # await client.get_channel(TEST_CHANNEL_ID).send(clues)
        detail = getDetail()
        await client.get_channel(TEST_CHANNEL_ID).send(f"```{detail}```")

# @tree.command(
#     name = "exchange",
#     description = "輸入線索",
#     guild=discord.Object(id=GUILD_ID)
# )
# async def first_command(interaction, arg: str):
#     exchange()
#     await interaction.response.send_message(f"計算完成")


@tree.command(
    name = "help",
    description = "各功能說明",
    guild=discord.Object(id=GUILD_ID)
)
async def first_command(interaction):
    await interaction.response.send_message(getHelp())


@tree.command(
    name = "clue",
    description = "設定線索, 格式: 玩家名稱, 線索",
    guild=discord.Object(id=GUILD_ID)
)
async def first_command(interaction, clue: str):
    setClues(clue)
    clues = getClues()
    await interaction.response.send_message(clues)

@tree.command(
    name = "clues",
    description = "顯示目前的線索清單",
    guild=discord.Object(id=GUILD_ID)
)
async def first_command(interaction):
    clues = getClues()
    await interaction.response.send_message(clues)

@tree.command(
    name = "users",
    description = "顯示玩家清單",
    guild=discord.Object(id=GUILD_ID)
)
async def first_command(interaction):
    users = getUsers()
    await interaction.response.send_message(users)

@tree.command(
    name = "result",
    description = "顯示計算結果",
    guild=discord.Object(id=GUILD_ID)
)
async def first_command(interaction):
    result = getResult()
    # await interaction.response.send_message(result)
    await client.get_channel(CLUE_CHANNEL_ID).send(result)


client.run(config['token'])