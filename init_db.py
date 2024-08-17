import sqlite3

db = sqlite3.connect("organizations.db")

with open('schema.sql') as f:
    db.executescript(f.read())
    
with open('languages.sql') as f:
    db.executescript(f.read())
    
with open('example.sql') as f:
    db.executescript(f.read())
    
