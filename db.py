import sqlite3

con = sqlite3.connect('spotify.db')  # Creates a new database file if it doesn’t exist
cur = con.cursor()

# create table statement
cur.execute("CREATE TABLE IF NOT EXISTS artist(name, num_albums, popularity)") # include if not exists to bypass the "table already exists" error message

def insert_artist(name, num_albums, popularity, con):
    with con:
        con.execute("INSERT INTO artist(name, num_albums, popularity) VALUES(?, ?, ?)", (name, num_albums, popularity))
    con.commit()

for row in cur.execute("SELECT name, num_albums, popularity FROM artist"):
    print(row)

con.close()