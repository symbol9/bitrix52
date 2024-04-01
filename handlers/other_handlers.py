import logging

from aiogram import Router
from aiogram.types import Message
from QA_Model.QA_Model import c

logger = logging.getLogger(__name__)

other_router = Router()


@other_router.message()
async def other_handlers(message: Message):
    content = message.text
    await message.answer(c(content=content).content)
