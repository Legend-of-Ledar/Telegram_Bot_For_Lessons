from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from .filters import IsUser
from telegram_bot.keyboards.registration_keyboards import subject_keyboard, days_keyboard, new_registration_keyboard
from telegram_bot.models.student import Student
from telegram_bot.config.config import CHAT_ID

router = Router()
router.message.filter(IsUser())
router.callback_query.filter(IsUser())


class Register(StatesGroup):
    name: State = State()
    subject: State = State()
    days: State = State()
    time_interval: State = State()


@router.message(CommandStart())
async def start_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Здравствуйте! Напишите ваше имя:")
    await state.set_state(Register.name)


@router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.subject)
    await message.answer("Выберите предмет:", reply_markup=subject_keyboard())


def is_subject(callback: CallbackQuery):
    return callback.data in ["subject_math", "subject_physics"]


def is_day_or_nav(callback: CallbackQuery):
    return callback.data.startswith("day_") or callback.data in ["back", "next"]


@router.callback_query(is_subject)
async def get_subject(callback: CallbackQuery, state: FSMContext):
    subject_map = {"subject_math": "Математика", "subject_physics": "Физика"}
    subject = subject_map.get(callback.data)
    await state.update_data(subject=subject)
    await state.set_state(Register.days)
    await show_days_keyboard(callback.message, state)
    await callback.answer()


async def show_days_keyboard(message: Message, state: FSMContext):
    data = await state.get_data()
    selected_days = data.get("days", [])
    await message.answer(
        "Выберите дни недели (можно несколько):",
        reply_markup=days_keyboard(selected_days)
    )


@router.callback_query(is_day_or_nav)
async def day_selection_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_days = data.get("days", [])

    if callback.data.startswith("day_"):
        day = callback.data.split("_")[1]
        if day in selected_days:
            selected_days.remove(day)
        else:
            selected_days.append(day)
        await state.update_data(days=selected_days)
        await show_days_keyboard(callback.message, state)

    elif callback.data == "next":
        if selected_days:
            await state.set_state(Register.time_interval)
            await callback.message.answer("Введите удобный интервал времени (например, 16:00-18:00):")
        else:
            await callback.answer("Выберите хотя бы один день", show_alert=True)

    elif callback.data == "back":
        await state.set_state(Register.subject)
        await callback.message.answer("Выберите предмет:", reply_markup=subject_keyboard())

    await callback.answer()


@router.message(Register.time_interval)
async def get_time_interval(message: Message, state: FSMContext):
    await state.update_data(time_interval=message.text)
    data = await state.get_data()

    student = Student(
        name=data.get("name"),
        subject=data.get("subject"),
        days=data.get("days", []),
        time=data.get("time_interval")
    )

    await message.answer(
        f"Спасибо!🤎{student.name}\nПредмет: {student.subject}\nДни: {', '.join(student.days)}\nВремя: {student.time}"
    )

    telegram_tag = f"@{message.from_user.username}" if message.from_user.username else f"ID:{message.from_user.id}"
    await message.bot.send_message(
        chat_id=CHAT_ID,
        text=f"Новая запись:\nИмя: {student.name}\nTelegram: {telegram_tag}\nПредмет: {student.subject}\nДни: {', '.join(student.days)}\nВремя: {student.time}"
    )

    await state.clear()
    await message.answer("Если хотите сделать ещё одну запись, нажмите кнопку ниже ⬇️",
                         reply_markup=new_registration_keyboard())


@router.callback_query()
async def new_registration(callback: CallbackQuery, state: FSMContext):
    if callback.data == "new_registration":
        await state.clear()
        await callback.message.answer("Здравствуйте! Напишите ваше имя:")
        await state.set_state(Register.name)
        await callback.answer()