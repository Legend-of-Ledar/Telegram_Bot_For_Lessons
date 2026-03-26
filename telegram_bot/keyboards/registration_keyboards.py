from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def subject_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Математика", callback_data="subject_math"),
            InlineKeyboardButton(text="Физика", callback_data="subject_physics")
        ]
    ])

def days_keyboard(selected_days: list):
    buttons = []
    for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]:
        text = f"{day} {'✅' if day in selected_days else ''}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"day_{day}")])
    # кнопки навигации
    buttons.append([
        InlineKeyboardButton(text="Назад", callback_data="back"),
        InlineKeyboardButton(text="Далее", callback_data="next")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def new_registration_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новая запись", callback_data="new_registration")]
    ])