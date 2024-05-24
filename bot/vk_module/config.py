import logging
from vkbottle import Bot, API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler

from bot.misc.env import VK


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

api = API(VK.TOKEN)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()

bot_vk = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)
