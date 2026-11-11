
import pytest
from hypothesis import given, strategies as st

from course_registration_parser import (
    format_course_code,
    total_credits,
    parse_student_record
)


# Test 1: Fuzz testing format_course_code
@given(st.one_of(st.text(), st.none()))
def test_format_course_code_no_crash(s):
    try:
        format_course_code(s)
    except Exception as e:
        pytest.fail(f"format_course_code crashed with input {s!r}: {e}")


# Test 2: Fuzz testing total_credits
@given(st.one_of(st.text(), st.none()))
def test_total_credits_no_crash(s):
    try:
        total_credits(s)
    except Exception as e:
        pytest.fail(f"total_credits crashed with input {s!r}: {e}")


# Test 3: Fuzz testing parse_student_record
@given(st.one_of(st.text(), st.none()))
def test_parse_student_record_no_crash(s):
    try:
        parse_student_record(s)
    except Exception as e:
        pytest.fail(f"parse_student_record crashed with input {s!r}: {e}")


# Test 4: Valid course code
def test_format_course_code_valid():
    assert format_course_code("cs 301") == "CS301"


# Test 5: Valid credit calculation
def test_total_credits_valid():
    assert total_credits("4,3,4") == 11


# Test 6: Valid student record
def test_parse_student_record_valid():
    result = parse_student_record("pes1ug23cs001|Asha|regular")

    assert result == {
        "srn": "PES1UG23CS001",
        "name": "Asha",
        "status": "regular"
    }


# Test 7: Invalid input handling
def test_invalid_inputs_are_handled():
    assert format_course_code(None) == ""
    assert format_course_code("cs") == ""
    assert format_course_code("cs 301 extra") == ""

    assert total_credits(None) == 0
    assert total_credits("") == 0
    assert total_credits("4,,3") == 0
    assert total_credits("one,two") == 0

    empty_record = {"srn": "", "name": "", "status": ""}

    assert parse_student_record(None) == empty_record
    assert parse_student_record("only|two") == empty_record
    assert parse_student_record("a|b|c|d") == empty_record
