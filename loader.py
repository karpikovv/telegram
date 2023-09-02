import sqlite3
from telebot import TeleBot
from config_data import config


connection = sqlite3.connect('database_history.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS History (
noteid INTEGER PRIMARY KEY,
chatid INTEGER NOT NULL,
name TEXT NOT NULL,
score INTEGER,
total INTEGER,
price REAL,
stars INTEGER,
distance REAL
)
''')

connection.commit()
connection.close()


bot = TeleBot(config.BOT_TOKEN)
print(2)