

def view_spam_tables_empty() -> str:
    return "Таблицы отсутствуют"


def select_spam_table_successful(spam_table_id: int, spam_table_name: str) -> str:
    return f"Вы выбрали таблицу: «{spam_table_name}» ({spam_table_id})"


def select_spam_table_empty() -> str:
    return "Такой таблицы не существует"
