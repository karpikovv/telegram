import sqlite3


def add_history(chat_id, name, score, total, price, stars, distance):
    connection = sqlite3.connect("database_history.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO History (chatid, name, score, total, price, stars, distance) VALUES(?,?,?,?,?,?,?)",
        (chat_id, name, score, total, price, stars, distance),
    )

    connection.commit()
    connection.close()
