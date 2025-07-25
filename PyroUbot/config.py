import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "500"))

DEVS = list(map(int, os.getenv("DEVS", "7735182806").split()))

API_ID = int(os.getenv("API_ID", "25874950"))

API_HASH = os.getenv("API_HASH", "24516ee5b21032f5f0f31f90725864f8")

BOT_TOKEN = os.getenv("BOT_TOKEN", "7449056036:AAF5ccRHvynrQ92D2NfyUxIJRogj1Hcww2M")

OWNER_ID = int(os.getenv("OWNER_ID", "7735182806"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002895302109").split()))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

MONGO_URL = os.getenv("mongodb+srv://ArmonSupport:<ArmonSupport>@armonsupport.vmhki35.mongodb.net/?retryWrites=true&w=majority&appName=ArmonSupport)

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-1002750737318"))
