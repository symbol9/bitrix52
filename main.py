import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis
from handlers import user_handlers, other_handlers
from config.config import load_config
from keyboards.main_menu import set_main_menu


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='{filename}:{lineno} {levelname:8s} '
               '[{asctime}] - {name} - {message}',
        style='{'
    )

    config = load_config()

    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.other_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
