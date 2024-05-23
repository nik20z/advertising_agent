from sqlite3 import Cursor

from bot.vk_module.database.connect import cursor


def check_error(func):
    """ Декоратор для проверки существования записи в таблице spam_config """
    def wrapper(*args, **kwargs) -> Cursor:
        return func(*args, **kwargs)

    return wrapper


def spam_config_table(admin_id: int, spam_table_id: int) -> Cursor:
    """ Обновить информацию о выбранной таблице для рассылки """
    return cursor.execute(f"UPDATE spam_config SET spam_table_id = {spam_table_id} WHERE admin_id = {admin_id}")
