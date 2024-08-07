import discord
import json
from discord import app_commands, Message, Interaction
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


# Load configuration
def load_config():
    with open("config.json", "r", encoding="utf8") as file:
        return json.load(file)


config = load_config()
print(config["token"])
print(config["GUILD_ID"])

# GUILD_ID=1063079372568924250
GUILD_ID = config["GUILD_ID"]
CLUE_CHANNEL_ID = config["CLUE_CHANNEL_ID"]
CHAT_CHANNEL_ID = config["CHAT_CHANNEL_ID"]
TEST_CHANNEL_ID = config["TEST_CHANNEL_ID"]

BOT_ID = 1087755638886645882
CHANNEL_HISTORY_LIMIT = 10  # 設定要讀取的歷史訊息數量

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
async def on_message(message: Message):
    if message.author == client.user:
        if message.content == "計算完成":
            result = getResult()
            await client.get_channel(CLUE_CHANNEL_ID).send(result)
        return

    print(message.author.id, message.author.name, message.content)
    print(message.channel.id)
    # print(message.guild.id)
    try:
        user = config["users"][str(message.author.id)]
        print(user)
    except:
        print("User not found in config")

    if message.content == "ping":
        await message.channel.send("pong")
    elif message.content == "exchange":
        exchange()
        await message.channel.send("計算完成")

    # update clues from history messages (today only)
    # TODO: 重複留言的話，以最後一則為主
    elif message.content == "update":
        channel = client.get_channel(CLUE_CHANNEL_ID)
        messages = [msg async for msg in channel.history(limit=CHANNEL_HISTORY_LIMIT)]

        for msg in messages:
            message_date = (
                msg.created_at + timedelta(hours=8)
            ).date()  # get msg date in Taiwan
            if date.today() == message_date and msg.author.id != BOT_ID:
                handle_clue_message(msg)

        # return updated clues
        detail = getDetail()
        await client.get_channel(TEST_CHANNEL_ID).send(
            f"```{detail}```用歷史訊息更新線索完成"
        )

    # 更新線索
    elif message.channel.id == CLUE_CHANNEL_ID:
        handle_clue_message(message)

        # return updated clues
        detail = getDetail()
        await client.get_channel(TEST_CHANNEL_ID).send(f"```{detail}```")


def handle_clue_message(message: Message):
    if message.author.id == 525463925194489876:  # 更新線索 (小蔡)
        handle_multiple_clue_message(message)
    else:
        handle_single_clue_message(message)


def handle_single_clue_message(message: Message):
    try:
        user = config["users"][str(message.author.id)]
        clues = formatClues(message.content)
        setClues(f"{user}, {clues}")
    except KeyError:
        print("User not found in config")


def handle_multiple_clue_message(message: Message):
    try:
        for i in range(2):
            clue = message.content.split("\n")[i]
            user, clue_content = clue.split(":")
            clues = formatClues(clue_content)
            setClues(f"{user}, {clues}")
    except IndexError as e:
        print(e)


# @tree.command(
#     name = "exchange",
#     description = "輸入線索",
#     guild=discord.Object(id=GUILD_ID)
# )
# async def first_command(interaction, arg: str):
#     exchange()
#     await interaction.response.send_message(f"計算完成")


@tree.command(name="help", description="各功能說明", guild=discord.Object(id=GUILD_ID))
async def show_help(interaction: Interaction):
    await interaction.response.send_message(getHelp())


@tree.command(
    name="clue",
    description="設定線索, 格式: 玩家名稱, 線索",
    guild=discord.Object(id=GUILD_ID),
)
async def set_user_clues(interaction: Interaction, text: str):
    user, clue = text.split(",", 1)
    setClues(f"{user}, {formatClues(clue)}")
    clues = getClues()
    await interaction.response.send_message(clues)


@tree.command(
    name="clues", description="顯示目前的線索清單", guild=discord.Object(id=GUILD_ID)
)
async def get_user_clues(interaction: Interaction):
    clues = getClues()
    await interaction.response.send_message(clues)


@tree.command(
    name="users", description="顯示玩家清單", guild=discord.Object(id=GUILD_ID)
)
async def get_all_users(interaction: Interaction):
    users = getUsers()
    await interaction.response.send_message(users)


@tree.command(
    name="result", description="顯示計算結果", guild=discord.Object(id=GUILD_ID)
)
async def get_calculate_result(interaction: Interaction):
    result = getResult()
    # await interaction.response.send_message(result)
    await client.get_channel(CLUE_CHANNEL_ID).send(result)


client.run(config["token"])
