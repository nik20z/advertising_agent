from sqlite3 import Row
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.tg_module.keyboards.my_callback import SelectSpamTableCallback, PaginationCallback, OtherCallback


_close_button = InlineKeyboardButton(text="❌", callback_data=OtherCallback(action="close").pack())


def _paging_button(element_id: int, direction: str) -> InlineKeyboardButton:
    """ Получить кнопку листания вправо-влево """
    direction_bool = {'previous': False, 'next': True}.get(direction, True)
    text = {'previous': '«', 'next': '»'}.get(direction)
    callback_data = PaginationCallback(element_id=element_id, direction_bool=direction_bool).pack()
    return InlineKeyboardButton(text=text, callback_data=callback_data)


def _back_button(last_callback_data: CallbackData) -> InlineKeyboardButton:
    """ Кнопка возврата """
    return InlineKeyboardButton(text="🔙", callback_data=last_callback_data.pack())


def personal_area(spam_table_name: str) -> InlineKeyboardMarkup:
    """ Личный кабинет """
    builder = InlineKeyboardBuilder()

    builder.button(text=str(spam_table_name), callback_data=OtherCallback(action="view_spam_tables").pack())
    builder.add(_close_button)
    builder.adjust(1, 1)

    return builder.as_markup()


def view_spam_tables(spam_table_list: list[Row]) -> InlineKeyboardMarkup:
    """ Список таблиц для рассылки """
    builder = InlineKeyboardBuilder()

    previous_spam_table = spam_table_list[0]
    next_spam_table = spam_table_list[-1]
    left_paging_btn = _paging_button(previous_spam_table['spam_table_id'], 'previous')
    right_paging_btn = _paging_button(next_spam_table['spam_table_id'], 'next')

    for spam_table in spam_table_list:
        spam_table_id = spam_table['spam_table_id']
        spam_table_name = spam_table['spam_table_name']
        callback_data = SelectSpamTableCallback(spam_table_id=spam_table_id).pack()
        builder.button(text=spam_table_name, callback_data=callback_data)

    builder.row(left_paging_btn, right_paging_btn)
    builder.row(_back_button(OtherCallback(action='personal_area')))

    return builder.as_markup()
