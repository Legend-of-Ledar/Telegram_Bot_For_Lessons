from dotenv import load_dotenv
import os

load_dotenv("telegram_bot/config/Token.env")

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")