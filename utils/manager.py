import sqlite3
import os

class Database:

	def __init__(self, path):
		if not os.path.exists(path):
			self.connection = create_connection(path)
			sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
											telegram_id integer PRIMARY KEY,
		 									language text DEFAULT "en",
		 									level int DEFAULT 3
										);"""
			create_table(self.connection, sql_create_users_table)

		self.connection = sqlite3.connect(path)


	def create_user(self, user):
		sql = """ INSERT INTO users(telegram_id) VALUES(?) """
		cur = self.connection.cursor()
		cur.execute(sql, (user,))
		return cur.lastrowid


	def select_language_by_telegram_id(self, telegram_id):
		cur = self.connection.cursor()
		cur.execute('SELECT language FROM users WHERE telegram_id=?', (telegram_id,))
		language = cur.fetchone()
		return language[0]


	def select_level_by_telegram_id(self, telegram_id):
		cur = self.connection.cursor()
		cur.execute('SELECT level FROM users WHERE telegram_id=?', (telegram_id,))
		level = cur.fetchone()
		return level[0]


	def update_user_language(self, user):
		sql_update_user = """ UPDATE users
							  SET language = ?
							  WHERE telegram_id = ? """

		cur = self.connection.cursor()
		cur.execute(sql_update_user, user)
		self.connection.commit()


	def update_user_level(self, user):
		sql_update_user = """ UPDATE users
							  SET level = ?
							  WHERE telegram_id = ? """

		cur = self.connection.cursor()
		cur.execute(sql_update_user, user)
		self.connection.commit()


	def user_exists(self, telegram_id):
		cur = self.connection.cursor()
		cur.execute('SELECT COUNT(*) FROM users WHERE telegram_id=?', (telegram_id,))
		exists = cur.fetchone()
		return bool(exists[0])


	def delete_user(self, user):
		cur = self.connection.cursor()
		cur.execute('DELETE FROM users WHERE telegram_id=?', user)
		self.connection.commit()