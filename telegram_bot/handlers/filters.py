from aiogram.filters import BaseFilter
from config.config import CHAT_ID

class IsUser(BaseFilter):
    async def __call__(self, event):
        user_id = getattr(event.from_user, "id", None)
        return user_id != CHAT_ID

class IsAdmin(BaseFilter):
    async def __call__(self, event):
        user_id = getattr(event.from_user, "id", None)
        return user_id == CHAT_ID