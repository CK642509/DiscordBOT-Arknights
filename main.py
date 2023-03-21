from discord.ext import commands 
import discord
import json


with open('items.json', "r", encoding = "utf8") as file:
    data = json.load(file)
print(data["token"])

#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('目前登入身份：', client.user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'ping':
        await message.channel.send('pong')

client.run(data['token'])