import sqlite3
from werkzeug.security import generate_password_hash


connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

cur.execute("INSERT INTO user (username, hash) VALUES (?, ?)",
            ('frank', generate_password_hash("1234")))

connection.commit()



connection.close()