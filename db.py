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

def artist_in_db(name):
    con = sqlite3.connect('spotify.db')
    cur = con.cursor()   

    cur.execute("SELECT 1 FROM artist WHERE name = ?", (name,))
    exists = cur.fetchone() is not None
    con.close()
    return exists

def delete_artist(name):
    con = sqlite3.connect('spotify.db')
    cur = con.cursor()

    cur.execute("DELETE FROM artist WHERE name = ?", (name,))  
    con.commit()
    con.close()

def delete_db():
    con = sqlite3.connect('spotify.db')
    cur = con.cursor() 

    cur.execute("DELETE FROM artist")

    con.commit()
    con.close()

# delete_db()
# print_artists_data()