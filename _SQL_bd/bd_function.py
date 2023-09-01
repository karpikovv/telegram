import sqlite3


def add_history(chat_id, name, score, total, price, stars, distance):
    connection = sqlite3.connect('database_history.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO History (chatid, name, score, total, price, stars, distance) VALUES(?,?,?,?,?,?,?)',
                   (chat_id, name, score, total, price, stars, distance))

    connection.commit()
    connection.close()


def get_history(chat_id):
    connection = sqlite3.connect('database_history.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM History WHERE chatid = ? ORDER BY noteid DESC', (chat_id,))
    history = cursor.fetchmany(24)
    connection.commit()
    connection.close()
    return history


def delete_history(chat_id):
    connection = sqlite3.connect('database_history.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM History WHERE chatid = ?', (chat_id,))

    connection.commit()
    connection.close()
