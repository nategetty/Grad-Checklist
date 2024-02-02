#
# test_module.py
#

from gradchecklist.module import *
from gradchecklist.course import get_v_course


def test_get_module(db):
    module = get_module(db, "HONOURS SPECIALIZATION IN COMPUTER SCIENCE")
    assert module is not None
    assert len(module.requirements) == 10
    assert module.requirements[0].courses


def test_get_module_no_records(db):
    assert get_module(db, "MAJOR IN PYTHON") is None


def clear_module_ids(module: Module):
    module.id = 0
    for req in module.requirements:
        req.id = 0
        req.module_id = 0


def test_insert_module(db):
    module = Module()
    module.name = "MAJOR IN TESTING"

    # Equivalent to: "0.5 course from: Computer Science 1027A/B or Computer Science 1037A/B (in either case with a mark of at least 65%)"
    req = ModuleRequirement(total_credit=0.5, minimum_grade=65, is_admission=True)
    req.courses = [
        get_v_course(db, "COMPSCI", 1027),
        get_v_course(db, "COMPSCI", 1037)
    ]
    module.requirements.append(req)

    insert_module(db, module)

    result = get_module(db, module.name)
    assert len(result.requirements) == 1
    assert result.requirements[0].courses == req.courses
