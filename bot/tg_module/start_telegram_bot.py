import asyncio
from aiogram import Bot
from aiogram.methods.set_my_commands import BotCommand

from bot.tg_module.database import Insert
from bot.misc.env import TG
from bot.tg_module.handlers import admin_router, user_router
from bot.tg_module.config import bot_tg, dp, my_commands_data_dict


async def set_default_commands(bot: Bot) -> bool:
    """ Установить дефолтные команды """
    command_list = []
    for command, descriptions in my_commands_data_dict.items():
        command_list.append(BotCommand(command=command, descriptions=descriptions))

    return await bot.set_my_commands(commands=command_list)


async def start_telegram_bot() -> None:
    Insert.add_all_admins_to_db(admin_ids=list(TG.ADMIN_LIST))

    dp.include_router(admin_router)
    dp.include_router(user_router)

    # await set_default_commands(bot_tg)
    # await bot_tg.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot_tg)


if __name__ == '__main__':
    asyncio.run(start_telegram_bot())
