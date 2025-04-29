import sqlite3

def initalize_db():
    con = sqlite3.connect('spotify.db')
    cur = con.cursor()
    # create table statement
    cur.execute("CREATE TABLE IF NOT EXISTS artist(name, num_albums, popularity)") # include if not exists to bypass the "table already exists" error message

def insert_artist(name, num_albums, popularity, con):
    con = sqlite3.connect('spotify.db')
    # cur = con.cursor()
    with con:
        con.execute("INSERT INTO artist(name, num_albums, popularity) VALUES(?, ?, ?)", (name, num_albums, popularity))
    con.commit()
    con.close()

def get_all_artists():
    con = sqlite3.connect('spotify.db')
    cur = con.cursor()
    
    cur.execute("SELECT name, num_albums, popularity FROM artist")
    rows = cur.fetchall()
    con.close()
    return rows

def print_artists_data():
    con = sqlite3.connect('spotify.db')
    cur = con.cursor()
    for row in cur.execute("SELECT name, num_albums, popularity FROM artist"):
        print(row)