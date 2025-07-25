# PyroUbot/__init__.py

# ---- Optional: uvloop (abaikan jika tidak tersedia) ----
try:
    import uvloop
    import asyncio
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    # Tidak apa-apa kalau gagal di Windows / Replit tertentu
    pass

import logging
import os

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls import filters as fl
from pyromod import listen
from aiohttp import ClientSession

from PyroUbot.config import *  # pastikan file config-mu ada & tidak error

# ---------- Logging ----------
class ConnectionHandler(logging.Handler):
    def emit(self, record):
        # Auto-restart ketika koneksi drop
        for X in ["OSError", "TimeoutError"]:
            if X in record.getMessage():
                os.system(f"kill -9 {os.getpid()} && python3 -m PyroUbot")

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

formatter = logging.Formatter(
    "[%(levelname)s] - %(name)s - %(message)s", "%d-%b %H:%M"
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

connection_handler = ConnectionHandler()

logger.addHandler(stream_handler)
logger.addHandler(connection_handler)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)

# ---------- Global aiohttp session ----------
aiosession = ClientSession()

# ---------- Bot wrapper ----------
class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func
        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func
        return decorator

    async def start(self):
        await super().start()
        # Tambahkan inisialisasi lain kalau perlu
        # misal: self.me = await self.get_me()
        # print(f"Logged in as {self.me.id} ({self.me.first_name})")

    async def stop(self, *args):
        await super().stop()
        await aiosession.close()