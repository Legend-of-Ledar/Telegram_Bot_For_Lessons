import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from handlers import registration, admin
from config.config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(registration.router)
dp.include_router(admin.router)

async def main():
    print("Бот запущен...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()  # закрываем сессию для безопасности

if __name__ == "__main__":
    asyncio.run(main())