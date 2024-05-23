import configparser
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.misc.env import TG


my_commands_data_dict = {
    'start': 'Запуск бота',
    'show_keyboard': 'Показать клавиатуру',
    'personal_area': 'Личный кабинет',
    'help': 'Помощь'
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)

dp = Dispatcher()

bot_tg = Bot(
    token=TG.TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
