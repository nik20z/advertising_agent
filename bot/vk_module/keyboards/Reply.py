from vkbottle import Keyboard
from vkbottle import Text


def default(one_time: bool = False) -> Keyboard:
    """ Дефолтная клавиатура """
    keyboard = Keyboard(one_time=one_time, inline=False)
    keyboard.add(Text('Личный кабинет'))
    return keyboard
