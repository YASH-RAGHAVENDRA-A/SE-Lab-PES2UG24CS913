
import pytest

from course_registration import (
    can_register,
    waitlist_position,
    late_fee,
)


def test_unknown_status():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("unknown", 0, 3, True)


def test_invalid_course_credits():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, -1, True)


def test_missing_prerequisites():
    assert can_register("regular", 0, 3, False) == "prerequisites missing"


def test_credit_limit_exceeded():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


def test_registration_exactly_at_credit_limit():
    assert can_register("regular", 20, 4, True) == "registered"


def test_waitlist_invalid_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, -1, 0)


def test_waitlist_seat_available():
    assert waitlist_position(9, 10, 0) == 0


def test_waitlist_at_capacity():
    assert waitlist_position(10, 10, 2) == 3


def test_waitlist_limit_reached():
    assert waitlist_position(10, 10, 10) == -1


def test_late_fee_zero_days():
    assert late_fee(0, 10, False) == 0


def test_late_fee_waiver():
    assert late_fee(5, 10, True) == 0


def test_late_fee_seven_days():
    assert late_fee(7, 10, False) == 500


def test_late_fee_more_than_seven_days():
    assert late_fee(8, 10, False) == 600


def test_credits_exactly_twenty():
    assert late_fee(5, 20, False) == 500


def test_credits_above_twenty():
    assert late_fee(5, 21, False) == 750


def test_fee_exactly_at_cap():
    assert late_fee(22, 25, False) == 2000


def test_fee_exceeds_cap():
    assert late_fee(30, 25, False) == 2000
