from vkbottle import CtxStorage
from vkbottle.bot import BotLabeler, Message, rules

from bot.vk_module import answers
from bot.vk_module.config import api


user_labeler = BotLabeler()
ctx_user_storage = CtxStorage()
AnswerText = answers.Text
AnswerCallback = answers.Callback

