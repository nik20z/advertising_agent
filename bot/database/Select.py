from sqlite3 import Cursor

from bot.database.connect import cursor


def spam_table(type_table: str) -> Cursor:
    """ Список таблиц для рассылки """
    return cursor.execute("SELECT * FROM spam_table WHERE name_social_network=?", (type_table,))


def check_exist_spam_table(spam_table_name: str) -> Cursor:
    """ Проверка существования таблицы по названию """
    return cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (spam_table_name,))


def user_ids_for_spamming(spam_table_name: str) -> Cursor:
    """ Получить список пользователей для рассылки из определенной таблицы """
    return cursor.execute(f"SELECT user_id FROM {spam_table_name}")
