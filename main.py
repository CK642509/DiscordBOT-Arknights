import discord
import json
from discord import app_commands
from datetime import date, timedelta

from utils import (
    exchange,
    getResult,
    getUsers,
    setClues,
    getClues,
    getDetail,
    getHelp,
    formatClues,
)


with open("config.json", "r", encoding="utf8") as file:
    config = json.load(file)
print(config["token"])
print(config["GUILD_ID"])

# GUILD_ID=1063079372568924250
GUILD_ID = config["GUILD_ID"]
CLUE_CHANNEL_ID = config["CLUE_CHANNEL_ID"]
CHAT_CHANNEL_ID = config["CHAT_CHANNEL_ID"]
TEST_CHANNEL_ID = config["TEST_CHANNEL_ID"]

# client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("目前登入身份：", client.user)


@client.event
async def on_message(message):
    if message.author == client.user and message.content == "計算完成":
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

    if message.content == "ping":
        await message.channel.send("pong")
    if message.content == "exchange":
        exchange()
        await message.channel.send("計算完成")
    if message.content == "update":
        limit = 10
        channel = client.get_channel(CLUE_CHANNEL_ID)
        messages = [message async for message in channel.history(limit=limit)]
        for i in range(limit):
            if (
                date.today() == (messages[i].created_at + timedelta(hours=8)).date()
            ):  # UTC+8
                if messages[i].author.id == 525463925194489876:  # 更新線索 (小蔡)
                    try:
                        for j in range(2):
                            clue = messages[i].content.split("\n")[j]
                            user = clue.split(":")[0]
                            clues = formatClues(clue.split(":")[1])
                            setClues(f"{user}, {clues}")
                    except IndexError as e:
                        print(e)
                elif messages[i].author.id != 1087755638886645882:  # BOT ID
                    user = config["users"][str(messages[i].author.id)]
                    clues = formatClues(messages[i].content)
                    setClues(f"{user}, {clues}")

        detail = getDetail()
        await client.get_channel(TEST_CHANNEL_ID).send(
            f"```{detail}```用歷史訊息更新線索完成"
        )
    # 更新線索
    if (
        message.channel.id == CLUE_CHANNEL_ID
        and message.author.id != 525463925194489876
    ):
        user = config["users"][str(message.author.id)]
        clues = formatClues(message.content)
        setClues(f"{user}, {clues}")
        detail = getDetail()
        await client.get_channel(TEST_CHANNEL_ID).send(f"```{detail}```")
    # 更新線索 (小蔡)
    if (
        message.channel.id == CLUE_CHANNEL_ID
        and message.author.id == 525463925194489876
    ):
        try:
            for i in range(2):
                clue = message.content.split("\n")[i]
                user = clue.split(":")[0]
                clues = formatClues(clue.split(":")[1])
                setClues(f"{user}, {clues}")
        except IndexError as e:
            print(e)

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


@tree.command(name="help", description="各功能說明", guild=discord.Object(id=GUILD_ID))
async def first_command(interaction):
    await interaction.response.send_message(getHelp())


@tree.command(
    name="clue",
    description="設定線索, 格式: 玩家名稱, 線索",
    guild=discord.Object(id=GUILD_ID),
)
async def first_command(interaction, text: str):
    user = text.split(",")[0]
    clue = text.split(",")[1]
    setClues(f"{user}, {formatClues(clue)}")
    clues = getClues()
    await interaction.response.send_message(clues)


@tree.command(
    name="clues", description="顯示目前的線索清單", guild=discord.Object(id=GUILD_ID)
)
async def first_command(interaction):
    clues = getClues()
    await interaction.response.send_message(clues)


@tree.command(
    name="users", description="顯示玩家清單", guild=discord.Object(id=GUILD_ID)
)
async def first_command(interaction):
    users = getUsers()
    await interaction.response.send_message(users)


@tree.command(
    name="result", description="顯示計算結果", guild=discord.Object(id=GUILD_ID)
)
async def first_command(interaction):
    result = getResult()
    # await interaction.response.send_message(result)
    await client.get_channel(CLUE_CHANNEL_ID).send(result)


client.run(config["token"])
