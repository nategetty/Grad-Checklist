#
# conftest.py
# Testing config.
#

import pytest
from gradchecklist.db import create_db_connection


# Creates database scehema (tables, views, etc) and inserts testing data.
def schema(db):
    with db.cursor() as c, open("sql/schema.sql") as schema, open("sql/testdata.sql") as testdata:
        queries = schema.read().split(";") + testdata.read().split(";")
        for query in queries:
            if not query.isspace():
                c.execute(query)
    db.commit()


# Deletes the database.
def drop_db(db):
    with db.cursor() as c:
        c.execute("DROP DATABASE gradchecklist") 
    db.commit()


# Creates database connection for tests.
@pytest.fixture
def db():
    # Connects to the database. Creates the database if it does not exist.
    try:
        db = create_db_connection(database="gradchecklist")
    except:
        db = create_db_connection(database="")
        schema(db)

    yield db

    # Resets the database after tests.
    drop_db(db)
    schema(db)
    db.close()
