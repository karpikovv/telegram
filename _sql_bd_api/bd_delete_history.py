import sqlite3


def delete_history(chat_id):
    connection = sqlite3.connect("database_history.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM History WHERE chatid = ?", (chat_id,))

    connection.commit()
    connection.close()
