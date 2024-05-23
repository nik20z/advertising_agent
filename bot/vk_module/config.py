import configparser
import os
from vkbottle import Bot, API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler

from bot.misc.env import VK


api = API(VK.TOKEN)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()

bot_vk = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)
