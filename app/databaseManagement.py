import sqlite3
from flask import g

DATABASE = 'organizations.db'

def init_app(app):
    app.teardown_appcontext(close_db)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    result = cur.fetchall()
    cur.close()
    return (result[0] if result else None) if one else result

def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()