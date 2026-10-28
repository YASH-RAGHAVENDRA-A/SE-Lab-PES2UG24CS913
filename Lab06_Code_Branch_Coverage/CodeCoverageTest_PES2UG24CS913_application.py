
import pytest

from course_registration import (
    can_register,
    waitlist_position,
    late_fee,
)


def test_successful_registration():
    assert can_register("regular", 20, 4, True) == "registered"


def test_unknown_student_status():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("invalid", 0, 3, True)


def test_invalid_course_credits():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, 0, True)


def test_missing_prerequisites():
    assert can_register("regular", 0, 3, False) == "prerequisites missing"


def test_credit_limit_exceeded():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


def test_honors_registration():
    assert can_register("honors", 20, 8, True) == "registered"


def test_invalid_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)


def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0


def test_normal_waitlist_position():
    assert waitlist_position(40, 40, 3) == 4


def test_full_waitlist():
    assert waitlist_position(40, 40, 10) == -1


def test_not_late():
    assert late_fee(0, 10, False) == 0


def test_late_fee_waiver():
    assert late_fee(5, 10, True) == 0


def test_late_fee_within_seven_days():
    assert late_fee(5, 10, False) == 500


def test_late_fee_after_seven_days():
    assert late_fee(10, 10, False) == 800


def test_additional_fee_for_high_credits():
    assert late_fee(5, 21, False) == 750


def test_late_fee_cap():
    assert late_fee(30, 25, False) == 2000
