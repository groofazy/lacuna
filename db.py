import sqlite3

con = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
cur = con.cursor()

# create table statement
cur.execute("CREATE TABLE artist(popularity)")

res = cur.execute("SELECT name FROM sqlite_master")
res.fetchone()
