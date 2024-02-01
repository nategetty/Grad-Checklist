#
# db.py
# Database connection.
#

from flask import current_app, g
from .config import DefaultConfig

try:
    import MySQLdb as mysql
    import MySQLdb.converters
except:
    import pymysql as mysql
    import pymysql.converters


# Returns a new database connection.
# Use get_db() instead when in the context of a request.
def create_db_connection(host=DefaultConfig.DB_HOST,
                         user=DefaultConfig.DB_USER,
                         password=DefaultConfig.DB_PASSWORD,
                         database=DefaultConfig.DB_DATABASE):
    mysql.converters.conversions[mysql.FIELD_TYPE.BIT] = lambda val: val == b"\x01"
    return mysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


# Returns database connection for the current request.
def get_db():
    if "db" not in g:
        g.db = create_db_connection(
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
