#
# test_module.py
#

from gradchecklist.module import *


def test_get_module(db):
    module = get_module(db, "MAJOR IN COMPUTER SCIENCE")
    assert module is not None
    assert len(module.requirements) == 6
    assert module.requirements[0].courses


def test_get_module_no_records(db):
    assert get_module(db, "MAJOR IN PYTHON") is None


def clear_module_ids(module: Module):
    module.id = 0
    for req in module.requirements:
        req.id = 0
        req.module_id = 0


def test_insert_module(db):
    module = get_module(db, "MAJOR IN COMPUTER SCIENCE")
    module.name = "MAJOR IN COMPUTER SCIENCE COPY"
    clear_module_ids(module)

    insert_module(db, module)

    result = get_module(db, module.name)
    clear_module_ids(result)
    
    assert result is not None
    assert result == module
