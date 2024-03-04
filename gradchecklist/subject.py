#
# subject.py
#

from dataclasses import dataclass
from typing import Optional


@dataclass
class Subject:
    code: str = ""
    name: str = ""
    category: Optional[str] = None
    category_2: Optional[str] = None


# Finds and returns the subject with the given code. Returns None if no matching subject is found.
def get_subject(db, code: str) -> Optional[Subject]:
    with db.cursor() as c:
        c.execute("SELECT * FROM Subject WHERE code=%s",
                  (code))
        subject = c.fetchone()
    if subject is None:
        return None
    else:
        return Subject(*subject)
    

# Returns list of all subject codes.
def get_all_subject_codes(db) -> list[Subject]:
    with db.cursor() as c:
        c.execute("SELECT code FROM Subject")
        subjects = c.fetchall()
    return [subject[0] for subject in subjects]


# Inserts subject into the database.
# Raises errors if the insert query fails.
def insert_subject(db, subject: Subject):
    try:
        with db.cursor() as c:
            c.execute("INSERT INTO Subject VALUES (%s,%s,%s,%s)",
                      list(vars(subject).values()))
        db.commit()
    except:
        db.rollback()
        raise
