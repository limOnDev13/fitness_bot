import asyncio
import logging.config

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import load_config, Config
from config.log_config import dict_config
import handlers.users_handlers


logging.config.dictConfig(dict_config)
logger = logging.getLogger("main")


async def main():
    logger.info("Starting bot")

    # get config
    config: Config = load_config()

    # init bot
    bot: Bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    # register handlers
    dp.include_router(handlers.users_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
