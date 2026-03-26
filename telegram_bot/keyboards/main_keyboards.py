from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новая запись", callback_data="new_registration")],
        [InlineKeyboardButton(text="Мои записи", callback_data="my_records")],
        [InlineKeyboardButton(text="Информация / Помощь", callback_data="info")]
    ]
)

cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена / Выйти", callback_data="cancel")]
    ]
)