import sqlite3


def create_connection(db_file):
	conn = sqlite3.connect(db_file)
	return conn


def create_table(conn, sql_create_table):
	cur = conn.cursor()
	cur.execute(sql_create_table)


def create_user(conn, user):
	sql = """ INSERT INTO users(telegram_id) VALUES(?) """
	cur = conn.cursor()
	cur.execute(sql, (user,))
	return cur.lastrowid


def select_language_by_telegram_id(conn, telegram_id):
	cur = conn.cursor()
	cur.execute('SELECT language FROM users WHERE telegram_id=?', (telegram_id,))
	language = cur.fetchone()
	return language[0]


# Database initialization 

# def main():
# 	database = r"users.db"
# 	conn = create_connection(database)
# 	sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
# 									id integer PRIMARY KEY,
# 									telegram_id integer,
# 									language text DEFAULT "en",
# 									level int DEFAULT 2 
# 								);"""
	
# 	create_table(conn, sql_create_users_table)

# 	with conn:
# 		pass


# if __name__ == "__main__":
# 	main()