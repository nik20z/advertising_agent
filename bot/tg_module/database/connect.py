import os
import sqlite3

from bot.misc.env import TG


current_directory = os.path.dirname(__file__)
database_path = os.path.join(current_directory, 'data', f"{TG.DATABASE_NAME}.db")

connection = sqlite3.connect(database_path)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()
