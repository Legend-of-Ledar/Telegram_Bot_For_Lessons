from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from .filters import IsAdmin

router = Router()
router.message.filter(IsAdmin())

@router.message(CommandStart())
async def start_admin_panel(message: Message):
    await message.answer("Вы админ. Здесь будут отображаться все заявки.")