from bot.vk_module.database import Insert
from bot.misc.env import VK
from bot.vk_module.handlers import admin_labeler, user_labeler
from bot.vk_module.config import bot_vk, labeler


if __name__ == '__main__':
    Insert.add_all_admins_to_db(admin_ids=list(VK.ADMIN_LIST))

    labeler.load(admin_labeler)
    labeler.load(user_labeler)

    bot_vk.run_forever()
