#
# db.py
# Database connection.
#

from flask import current_app, g
import MySQLdb
import MySQLdb.converters


# Returns a database cursor.
def get_db():
    if "db" not in g:
        MySQLdb.converters.conversions[MySQLdb.FIELD_TYPE.BIT] = lambda val: val == b"\x01"
        g.db = MySQLdb.connect(
            host=current_app.config["DB_HOST"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_DATABASE"]
        )
    return g.db


# Closes the database connection.
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Initialises database access for an app.
def init_app(app):
    app.teardown_appcontext(close_db)
