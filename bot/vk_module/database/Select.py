from sqlite3 import Cursor
from typing import Optional

from bot.vk_module.database.connect import cursor
from bot.vk_module.database.utils import check_error


@check_error
def query(q: str) -> Cursor:
    """ Произвольный запрос """
    return cursor.execute(q)


@check_error
def spam_config_by_admin_id(admin_id: int) -> Cursor:
    """  """
    query = "SELECT * FROM spam_config WHERE admin_id = ?;"
    return cursor.execute(query, (admin_id,))


@check_error
def spam_table(table_title: Optional[str] = None, spam_table_id: Optional[int] = None) -> Cursor:
    """ Список таблиц для рассылки """
    query = "SELECT * FROM spam_table WHERE True"
    params = []

    if table_title is not None:
        query += " AND title = ?"
        params.append(table_title)

    if spam_table_id is not None:
        query += " AND spam_table_id = ?"
        params.append(spam_table_id)

    if not params:
        return cursor.execute(query)

    return cursor.execute(query, params)


@check_error
def check_exist_spam_table(spam_table_name: Optional[str]) -> Cursor:
    """ Проверка существования таблицы по названию """
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
    return cursor.execute(query, (spam_table_name,))


@check_error
def user_ids_for_spamming(table_title: Optional[str]) -> Cursor:
    """ Получить список пользователей для рассылки из определенной таблицы """
    query = f"SELECT user_id FROM {table_title};"
    return cursor.execute(query)
