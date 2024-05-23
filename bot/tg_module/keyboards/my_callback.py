from typing import Optional, Union

from aiogram.filters.callback_data import CallbackData


class PaginationCallback(CallbackData, prefix="pag"):
    """ Пагинация """
    element_id: int = 0
    direction_bool: bool = True


class SelectSpamTableCallback(CallbackData, prefix="sst"):
    """ Выбор таблицы для рассылки """
    spam_table_id: int = 0


class OtherCallback(CallbackData, prefix="oth"):
    """ Прочие колбэки """
    action: str = ''
    value: Optional[Union[str, bool, int, float]] = None
