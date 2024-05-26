from os import environ
from typing import Final


class VK:
    TOKEN: Final = environ.get('VK_TOKEN', '')
    TOKEN_VERSION: Final = environ.get('VK_TOKEN_VERSION', '5.199')
    BOT_ID: Final = environ.get('VK_BOT_ID', '')

    GOD_ID: Final = environ.get('VK_GOD_ID', 1)
    ADMIN_LIST = frozenset((GOD_ID,))

    DATABASE_NAME: Final = environ.get('VK_DATABASE_NAME', 'vkontakte')


class TG:
    TOKEN: Final = environ.get('TG_TOKEN', '')
    BOT_ID: Final = environ.get('TG_BOT_ID', '')

    GOD_ID: Final = environ.get('TG_GOD_ID', 1)
    ADMIN_LIST = frozenset((GOD_ID,))

    DATABASE_NAME: Final = environ.get('TG_DATABASE_NAME', 'telegram')

