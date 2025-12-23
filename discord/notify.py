from VersaLog import *
import api_req
from dotenv import load_dotenv

import discord
import asyncio
import os

logger = VersaLog(enum="detailed", show_tag=True, tag="Request")

load_dotenv()

TOKEN = os.getenv("Token")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)

async def send_to_all_guilds(message: str):
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                try:
                    await channel.send(message)
                    logger.info(f"{guild.name} / {channel.name} に送信成功")
                    return
                except Exception as e:
                    logger.error(f"{guild.name} に送信失敗: {e}")

async def log_and_send(level: str, message: str):
    if level == "info":
        logger.info(message)
    elif level == "error":
        logger.error(message)
    elif level == "warn":
        logger.warn(message)

    await send_to_all_guilds(f"[{level.upper()}]\n{message}")

async def weather_task():
    await client.wait_until_ready()

    success, result = api_req.get_weather(
        location="Tokyo",
        api_key=WEATHER_API_KEY
    )

    if success:
        await log_and_send("info", result)
    else:
        await log_and_send("error", result)

async def update_status():
    await client.wait_until_ready()

    while not client.is_closed():
        guild_count = len(client.guilds)
        await client.change_presence(
            activity=discord.Game(name=f"{guild_count} サーバーで稼働中")
        )
        logger.info(f"ステータス更新: {guild_count} サーバー")
        await asyncio.sleep(300)

@client.event
async def on_ready():
    logger.info(f"Bot起動: {client.user} / {len(client.guilds)} サーバー")

    client.loop.create_task(update_status())
    client.loop.create_task(weather_task())

client.run(TOKEN)
