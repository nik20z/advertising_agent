from sqlite3 import Row

from vkbottle import Keyboard
from vkbottle import Callback


_close_button = Callback('❌', {'cmd': 'close'})


def _paging_button(callback: str, direction: str) -> Callback:
    """Получить кнопку листания вправо-влево"""
    direction_bool = {'previous': False, 'next': True}.get(direction, True)
    text = {'previous': '«', 'next': '»'}.get(direction)
    return Callback(text, {'cmd': f"{callback}:{direction_bool}"})


def _back_button(last_callback_data: dict) -> Callback:
    """ Кнопка возврата """
    return Callback("🔙", last_callback_data)  # 🔙⬅◀


def personal_area(spam_table_name: str) -> str:
    """ Личный кабинет """
    keyboard = Keyboard(inline=True)
    keyboard.add(Callback(spam_table_name, {'cmd': 'view_spam_tables'}))
    keyboard.row()
    keyboard.add(_close_button)

    return keyboard.get_json()


def view_spam_tables(spam_table_list: list[Row]) -> str:
    """ Список таблиц для рассылки """
    keyboard = Keyboard(inline=True)

    previous_spam_table = spam_table_list[0]
    next_spam_table = spam_table_list[-1]
    left_paging_btn = _paging_button(previous_spam_table['spam_table_id'], 'previous')
    right_paging_btn = _paging_button(next_spam_table['spam_table_id'], 'next')

    for spam_table in spam_table_list:
        spam_table_id = spam_table['spam_table_id']
        spam_table_name = spam_table['spam_table_name']
        callback_data = {'select_spam_table': spam_table_id}
        keyboard.add(Callback(spam_table_name, callback_data))

        keyboard.row()

    keyboard.add(left_paging_btn)
    keyboard.add(right_paging_btn)
    keyboard.row()
    keyboard.add(_back_button({'cmd': 'personal_area'}))

    return keyboard.get_json()
