from os import environ
from typing import Final


class VK:
    TOKEN: Final = environ.get('VK_TOKEN', '')
    TOKEN_VERSION: Final = environ.get('VK_TOKEN_VERSION', '5.199')
    BOT_ID: Final = environ.get('VK_BOT_ID', '')

    GOD_ID: Final = environ.get('VK_GOD_ID', 264311526)
    ADMIN_LIST = frozenset((264311526,))


class TG:
    TOKEN: Final = environ.get('TG_TOKEN', '')
    # BOT_ID: Final = environ.get('TG_BOT_ID', '')


class DATABASE:
    NAME: Final = environ.get('DATABASE_NAME', 'advertising_agent')

