from bot.vk_module.config import labeler, bot
from bot.vk_module.handlers import admin_labeler, user_labeler

labeler.load(admin_labeler)
labeler.load(user_labeler)


def start_vk_bot():
    bot.run_forever()
