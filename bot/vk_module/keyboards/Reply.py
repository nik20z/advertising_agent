from vkbottle import Keyboard
from vkbottle import Text


def select_spam_table(spam_table_list: list) -> Keyboard:
    """ Клавиатура для выбора таблицы для рассылки """
    keyboard = Keyboard(one_time=False, inline=False)

    for spam_table in spam_table_list:
        keyboard.add(Text(spam_table['title']))
        if spam_table != spam_table_list[-1]:
            keyboard.row()

    return keyboard

