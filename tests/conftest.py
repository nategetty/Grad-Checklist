#
# conftest.py
# Testing config.
#

import pytest
import subprocess
from gradchecklist.db import create_db_connection


# TEMPORARY - to be replaced by module parser
# Hard-coded Honours Spec in CS module for testing.
from decimal import Decimal
from gradchecklist.module import Module, ModuleRequirement, insert_module
from gradchecklist.course import get_v_course
def create_test_module(db):
    module = Module(name="HONOURS SPECIALIZATION IN COMPUTER SCIENCE")
    module.requirements = [
        ModuleRequirement(
            total_credit=Decimal(0.5),
            minimum_grade=65,
            is_admission=True,
            courses=[
                get_v_course(db, "COMPSCI", 1025),
                get_v_course(db, "COMPSCI", 1026),
                get_v_course(db, "DATASCI", 1200),
                get_v_course(db, "ENGSCI", 1036)
            ]
        ),
        ModuleRequirement(
            total_credit=Decimal(0.5),
            minimum_grade=65,
            is_admission=True,
            courses=[
                get_v_course(db, "COMPSCI", 1027),
                get_v_course(db, "COMPSCI", 1037)
            ]
        ),
        ModuleRequirement(
            total_credit=Decimal(1.0),
            is_admission=True,
            courses=[
                get_v_course(db, "APPLMATH", 1201),
                get_v_course(db, "CALCULUS", 1000),
                get_v_course(db, "CALCULUS", 1301),
                get_v_course(db, "CALCULUS", 1500),
                get_v_course(db, "CALCULUS", 1501),
                get_v_course(db, "MATH", 1600),
                get_v_course(db, "NMM", 1411),
                get_v_course(db, "NMM", 1412),
                get_v_course(db, "NMM", 1414)
            ]
        ),
        ModuleRequirement(
            total_credit=Decimal(5.5),
            courses=[
                get_v_course(db, "COMPSCI", 2208),
                get_v_course(db, "COMPSCI", 2209),
                get_v_course(db, "COMPSCI", 2210),
                get_v_course(db, "COMPSCI", 2211),
                get_v_course(db, "COMPSCI", 2212),
                get_v_course(db, "COMPSCI", 3305),
                get_v_course(db, "COMPSCI", 3307),
                get_v_course(db, "COMPSCI", 3331),
                get_v_course(db, "COMPSCI", 3340),
                get_v_course(db, "COMPSCI", 3342),
                get_v_course(db, "COMPSCI", 3350)
            ]
        ),
        ModuleRequirement(
            total_credit=Decimal(0.5),
            courses=[
                get_v_course(db, "COMPSCI", 2214),
                get_v_course(db, "MATH", 2155)
            ]
        ),
        ModuleRequirement(
            total_credit=Decimal(0.5),
            courses=[
                get_v_course(db, "WRITING", 2101),
                get_v_course(db, "WRITING", 2111),
                get_v_course(db, "WRITING", 2125),
                get_v_course(db, "WRITING", 2131)
            ]
        ),
        ModuleRequirement(
            total_credit=Decimal(0.5),
            courses=[
                get_v_course(db, "COMPSCI", 4490)
            ]
        ),
        ModuleRequirement(
            total_credit=Decimal(1.0),
            courses=[
                get_v_course(db, "DATASCI", 3000)
            ]
        ),
        ModuleRequirement(
            total_credit=Decimal(0.5),
            courses=[
                get_v_course(db, "SCIENCE", 3377),
                get_v_course(db, "MATH", 2156),
                get_v_course(db, "MATH", 3159)
            ]
        ),
        ModuleRequirement(
            total_credit=Decimal(0.5),
            courses=[
                get_v_course(db, "STATS", 2141),
                get_v_course(db, "STATS", 2244),
                get_v_course(db, "BIOLOGY", 2244),
                get_v_course(db, "STATS", 2857)
            ]
        )
    ]
    insert_module(db, module)


# Loads database schema and data from backup.
def load_db_backup():
    subprocess.run('mysql -u root gradchecklist < sql/dump.sql', shell=True)


# Deletes and recreates the database.
def reset_db(db):
    with db.cursor() as c:
        c.execute("DROP DATABASE IF EXISTS gradchecklist")
        c.execute("CREATE DATABASE gradchecklist")
        c.execute("USE gradchecklist")
    db.commit()
    load_db_backup()


# Creates database connection for tests.
@pytest.fixture
def db():
    db = create_db_connection(database="")
    reset_db(db)

    yield db

    # Resets the database after tests.
    reset_db(db)
    db.close()
