from sqlite3 import Cursor


def check_error(func):
    """ Декоратор для обработки ошибок при отправке запросов """
    def wrapper(*args, **kwargs) -> Cursor:
        try:
            return func(*args, **kwargs)
        finally:
            pass

    return wrapper
