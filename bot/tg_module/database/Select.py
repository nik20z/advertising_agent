from sqlite3 import Cursor
from typing import Optional

from bot.tg_module.database.connect import cursor
from bot.tg_module.database.utils import check_error


@check_error
def query(q: str) -> Cursor:
    """ Произвольный запрос """
    return cursor.execute(q)


@check_error
def spam_config_by_admin_id(admin_id: int) -> Cursor:
    """ Получить конфиг для определенного админа """
    sql_query = "SELECT * FROM spam_config WHERE admin_id = ?;"
    return cursor.execute(sql_query, (admin_id,))


@check_error
def spam_table(table_title: Optional[str] = None, spam_table_id: Optional[int] = None) -> Cursor:
    """ Список таблиц для рассылки """
    sql_query = "SELECT * FROM spam_table WHERE True"
    params = []

    if table_title is not None:
        sql_query += " AND title = ?"
        params.append(table_title)

    if spam_table_id is not None:
        sql_query += " AND spam_table_id = ?"
        params.append(spam_table_id)

    if not params:
        return cursor.execute(sql_query)

    return cursor.execute(sql_query, params)


@check_error
def check_exist_spam_table(spam_table_name: Optional[str]) -> Cursor:
    """ Проверка существования таблицы по названию """
    sql_query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
    return cursor.execute(sql_query, (spam_table_name,))


@check_error
def user_ids_for_spamming(table_title: Optional[str]) -> Cursor:
    """ Получить список пользователей для рассылки из определенной таблицы """
    sql_query = f"SELECT user_id FROM {table_title};"
    return cursor.execute(sql_query)
