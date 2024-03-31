import logging

from aiogram import Router
from aiogram.types import Message

logger = logging.getLogger(__name__)

other_router = Router()


@other_router.message()
async def other_handlers(message: Message):
    await message.answer(text='Данное сообщение не поддерживается')