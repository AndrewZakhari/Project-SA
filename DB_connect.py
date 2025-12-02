from flask import Flask
import sqlite3
from flask_session import Session


app = Flask(__name__)

app.secret_key = 'super_secret_key'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "my_portal.db"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


class SQLiteCursor:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.description = None

    def execute(self, query, args=None):
        # Replace %s with ? for SQLite compatibility
        query = query.replace('%s', '?')
        if args:
            self.cursor.execute(query, args)
        else:
            self.cursor.execute(query)
        self.description = self.cursor.description
        return self.cursor

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
    
    @property
    def lastrowid(self):
        return self.cursor.lastrowid

class SQLiteConnectionWrapper:
    def __init__(self, connection):
        self.connection = connection

    def cursor(self):
        return SQLiteCursor(self.connection)

    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.connection.close()

class MySQL:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.teardown_appcontext(self.teardown)

    @property
    def connection(self):
        from flask import g
        if 'db' not in g:
            g.db = sqlite3.connect(self.app.config['MYSQL_DB'], check_same_thread=False)
            g.db.create_function("CONCAT", -1, lambda *args: "".join(str(arg) if arg is not None else "" for arg in args))
        return SQLiteConnectionWrapper(g.db)

    def teardown(self, exception):
        from flask import g
        db = g.pop('db', None)
        if db is not None:
            db.close()


mysql = MySQL(app)
Session(app)
