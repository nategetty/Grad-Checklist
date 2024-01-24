#
# conftest.py
# Testing config.
#

import pytest
from gradchecklist.db import create_db_connection


@pytest.fixture
def db():
    db = create_db_connection()
    with db.cursor() as c:
        c.execute(open("sql/clean.sql").read())
        c.execute(open("sql/schema.sql").read())
        c.execute(open("sql/testdata.sql").read())
    db.commit()
    yield db
    db.close()
