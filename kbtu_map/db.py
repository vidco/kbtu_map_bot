import logging
import os
import sqlite3

from kbtu_map.settings import USERS_PATH

LOG = logging.getLogger('db')


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
class Database:
	__instance = None

	@staticmethod
	def get_instance():
		if Database.__instance is None:
			Database(USERS_PATH)

		return Database.__instance

	def __init__(self, path):
		"""
		Do not call constructor of this class, it is singleton
		"""
		if Database.__instance is not None:
			raise Exception("This class is a singleton!")

		self.path = path

		LOG.info(f'Connected to database ({id(self)})')

		if not os.path.exists(path):
			query = '''CREATE TABLE IF NOT EXISTS users (
							telegram_id integer PRIMARY KEY,
							language text DEFAULT "kz",
							level int DEFAULT 0
						);'''

			with sqlite3.connect(self.path) as connection:

				cursor = connection.cursor()
				cursor.execute(query)

				connection.commit()

			LOG.info('Table users created')

		Database.__instance = self

	def create_user(self, user):
		query = 'INSERT INTO users(telegram_id) VALUES(?)'

		with sqlite3.connect(self.path) as connection:
			cursor = connection.cursor()
			cursor.execute(query, (user,))

			connection.commit()

			LOG.info(f'User with telegram id {cursor.lastrowid} registered')

		return cursor.lastrowid

	def select_language_by_telegram_id(self, telegram_id):
		query = 'SELECT language FROM users WHERE telegram_id=?'

		with sqlite3.connect(self.path) as connection:
			cursor = connection.cursor()
			cursor.execute(query, (telegram_id,))

			language = cursor.fetchone()

		if language:
			return language[0]
		return None

	def select_level_by_telegram_id(self, telegram_id):
		query = 'SELECT level FROM users WHERE telegram_id=?'

		with sqlite3.connect(self.path) as connection:
			cursor = connection.cursor()
			cursor.execute(query, (telegram_id,))

			level = cursor.fetchone()

		return level[0]

	def update_user_language(self, telegram_id, language):
		query = 'UPDATE users SET language = ? WHERE telegram_id = ?'

		with sqlite3.connect(self.path) as connection:
			cursor = connection.cursor()
			cursor.execute(query, (language, telegram_id))

			connection.commit()

	def update_user_level(self, telegram_id, level):
		query = 'UPDATE users SET level = ? WHERE telegram_id = ?'

		with sqlite3.connect(self.path) as connection:
			cursor = connection.cursor()
			cursor.execute(query, (level, telegram_id))

			connection.commit()

	def user_exists(self, telegram_id):
		query = 'SELECT count(*) FROM users WHERE telegram_id=?'

		with sqlite3.connect(self.path) as connection:
			cursor = connection.cursor()
			cursor.execute(query, (telegram_id,))

			exists = cursor.fetchone()

		return bool(exists[0])
