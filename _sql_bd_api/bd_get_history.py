import sqlite3


def get_history(chat_id):
    connection = sqlite3.connect("database_history.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM History WHERE chatid = ? ORDER BY noteid DESC", (chat_id,)
    )
    history = cursor.fetchmany(24)
    connection.commit()
    connection.close()
    return history
