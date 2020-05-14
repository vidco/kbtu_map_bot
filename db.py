import logging
import os
import sqlite3

logging.basicConfig(format='%(asctime)s [%(name)s] [%(levelname)s] - %(message)s', level=logging.INFO)
LOG = logging.getLogger('db')


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
class Database:

	def __init__(self, path):
		self.path = path

		LOG.info('Connected to database')

		if not os.path.exists(path):
			connection = sqlite3.connect(path)

			query = '''CREATE TABLE IF NOT EXISTS users (
							telegram_id integer PRIMARY KEY,
		 					language text DEFAULT "kz",
		 					level int DEFAULT 0
						);'''
			cursor = connection.cursor()
			cursor.execute(query)

			LOG.info('Table users created')
			connection.close()

	def create_user(self, user):
		connection = sqlite3.connect(self.path)

		query = 'INSERT INTO users(telegram_id) VALUES(?)'
		cursor = connection.cursor()
		cursor.execute(query, (user,))

		connection.commit()
		connection.close()

		LOG.info(f'User with telegram id {cursor.lastrowid} registered')
		return cursor.lastrowid

	def select_language_by_telegram_id(self, telegram_id):
		connection = sqlite3.connect(self.path)

		query = 'SELECT language FROM users WHERE telegram_id=?'
		cursor = connection.cursor()
		cursor.execute(query, (telegram_id,))

		language = cursor.fetchone()

		connection.close()

		return language[0]

	def select_level_by_telegram_id(self, telegram_id):
		connection = sqlite3.connect(self.path)

		query = 'SELECT level FROM users WHERE telegram_id=?'
		cursor = connection.cursor()
		cursor.execute(query, (telegram_id,))

		level = cursor.fetchone()

		connection.close()

		return level[0]

	def update_user_language(self, user):
		connection = sqlite3.connect(self.path)

		query = '''UPDATE users
					SET language = ?
					WHERE telegram_id = ?'''
		cursor = connection.cursor()
		cursor.execute(query, user)

		connection.commit()
		connection.close()

	def update_user_level(self, user):
		connection = sqlite3.connect(self.path)

		query = '''UPDATE users
					SET level = ?
					WHERE telegram_id = ?'''
		cursor = connection.cursor()
		cursor.execute(query, user)

		connection.commit()
		connection.close()

	def user_exists(self, telegram_id):
		connection = sqlite3.connect(self.path)

		query = 'SELECT COUNT(*) FROM users WHERE telegram_id=?'
		cursor = connection.cursor()
		cursor.execute(query, (telegram_id,))

		exists = cursor.fetchone()
		connection.close()

		return bool(exists[0])

	def delete_user(self, user):
		connection = sqlite3.connect(self.path)

		query = 'DELETE FROM users WHERE telegram_id=?'
		cur = connection.cursor()
		cur.execute(query, user)

		connection.commit()
		connection.close()

		LOG.info(f'User with telegram id {cursor.lastrowid} unregistered')
