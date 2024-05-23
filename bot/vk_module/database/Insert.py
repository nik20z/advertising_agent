from bot.vk_module.database.connect import cursor, connection


def add_all_admins_to_db(admin_ids: list[int]) -> None:
    """ Добавляем всех администраторов в таблицу """
    query = "INSERT INTO spam_config (admin_id) VALUES (?) ON CONFLICT (admin_id) DO NOTHING"
    params = [(admin_id,) for admin_id in admin_ids]
    cursor.executemany(query, params)
    connection.commit()
