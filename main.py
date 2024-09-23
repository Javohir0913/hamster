import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNetworkError
from aiogram.types import BotCommand


from config import BOT_TOKEN
from handlers.cmd_handlers import cmd_router

CHAT_ID = '6558646963'  # Bu yerni o'zingizning chat ID bilan almashtiring


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        await bot.set_my_commands(
            commands=[BotCommand(command='start', description='boshlash'),
                      ]
        )
        dp = Dispatcher()
        dp.include_router(cmd_router)

        # Har kuni ertalab 07:00 da ishlaydigan funksiya

        await dp.start_polling(bot, skip_updates=True)
    except TelegramNetworkError as e:
        logging.error(f"Network error occurred: {e}")
        logging.error("Unable to connect to Telegram API. Please check your network connection and bot token.")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
    finally:
        # Close the aiohttp client session properly
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
