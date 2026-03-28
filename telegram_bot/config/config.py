from dotenv import load_dotenv
import os

load_dotenv("Token.env")

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
