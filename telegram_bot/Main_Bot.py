import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import TOKEN
from handlers import registration, admin

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