"""Loan eligibility and EMI calculator with safer coding practices."""

import json
import math
import os
import secrets
import smtplib
from datetime import datetime
from email.message import EmailMessage

import paramiko


MAX_FOIR = 0.5
SUPPORTED_LOAN_TYPES = {"home", "car", "personal"}

applications: dict[str, dict[str, object]] = {}


def is_valid_number(value: object) -> bool:
    """Return True if a value is a finite number, excluding booleans."""
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def calculate_emi(
    principal: float,
    annual_rate: float,
    years: int,
) -> float:
    """Calculate monthly EMI using a decimal annual interest rate."""
    if not is_valid_number(principal) or principal <= 0:
        raise ValueError("Principal must be greater than zero.")

    if not is_valid_number(annual_rate) or annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if not isinstance(years, int) or isinstance(years, bool):
        raise ValueError("Loan tenure must be a positive integer.")

    if years <= 0:
        raise ValueError("Loan tenure must be positive.")

    months = years * 12
    monthly_rate = annual_rate / 12

    if monthly_rate == 0:
        return principal / months

    factor = (1 + monthly_rate) ** months

    return principal * monthly_rate * factor / (factor - 1)


def check_eligibility(
    age: int,
    income: float,
    credit_score: int,
    existing_emi: float,
    loan_type: str,
) -> bool:
    """Check all mandatory eligibility conditions."""
    valid_age = (
        isinstance(age, int)
        and not isinstance(age, bool)
        and 21 <= age <= 60
    )

    valid_income = (
        is_valid_number(income)
        and income > 0
    )

    valid_score = (
        is_valid_number(credit_score)
        and 300 <= credit_score <= 900
    )

    valid_existing_emi = (
        is_valid_number(existing_emi)
        and existing_emi >= 0
    )

    valid_loan_type = (
        isinstance(loan_type, str)
        and loan_type.strip().lower() in SUPPORTED_LOAN_TYPES
    )

    checks_valid = (
        valid_age
        and valid_income
        and valid_score
        and valid_existing_emi
        and valid_loan_type
    )

    if not checks_valid:
        return False

    return (
        existing_emi / income <= MAX_FOIR
        and (credit_score > 750 or income > 25000)
    )


def max_loan_amount(
    income: float,
    existing_emi: float,
    annual_rate: float,
    years: int,
) -> float:
    """Estimate the maximum loan principal from payment capacity."""
    if not is_valid_number(income) or income <= 0:
        raise ValueError("Income must be greater than zero.")

    if not is_valid_number(existing_emi) or existing_emi < 0:
        raise ValueError("Existing EMI cannot be negative.")

    if not is_valid_number(annual_rate) or annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if not isinstance(years, int) or isinstance(years, bool):
        raise ValueError("Loan tenure must be a positive integer.")

    if years <= 0:
        raise ValueError("Loan tenure must be positive.")

    available_payment = income * MAX_FOIR - existing_emi

    if available_payment <= 0:
        return 0.0

    months = years * 12
    monthly_rate = annual_rate / 12

    if monthly_rate == 0:
        return available_payment * months

    discount_factor = (1 + monthly_rate) ** (-months)

    return (
        available_payment
        * (1 - discount_factor)
        / monthly_rate
    )


def amortisation_schedule(
    principal: float,
    annual_rate: float,
    years: int,
) -> list[tuple[int, float, float]]:
    """Return monthly rows containing month, interest and balance."""
    emi = calculate_emi(principal, annual_rate, years)
    monthly_rate = annual_rate / 12
    balance = principal
    rows = []

    for month in range(1, years * 12 + 1):
        interest = balance * monthly_rate
        principal_paid = emi - interest
        balance = max(0.0, balance - principal_paid)

        rows.append(
            (month, round(interest, 2), round(balance, 2))
        )

    return rows


def application_id() -> str:
    """Generate a loan application identifier."""
    number = secrets.randbelow(90_000_000) + 10_000_000
    return f"LN-{number}"


def save_application(
    name: str,
    amount: float,
    file: str = "loans.json",
) -> str:
    """Save application records in JSON format."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Applicant name cannot be empty.")

    if not is_valid_number(amount) or amount <= 0:
        raise ValueError("Loan amount must be greater than zero.")

    if os.path.exists(file):
        load_applications(file)

    app_id = application_id()

    applications[app_id] = {
        "name": name.strip(),
        "amount": amount,
        "date": datetime.now().isoformat(timespec="seconds"),
    }

    try:
        with open(file, "w", encoding="utf-8") as file_handle:
            json.dump(applications, file_handle, indent=2)
    except OSError:
        applications.pop(app_id, None)
        raise

    return app_id


def load_applications(
    file: str = "loans.json",
) -> dict[str, dict[str, object]]:
    """Load valid application records from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as file_handle:
            loaded = json.load(file_handle)
    except FileNotFoundError:
        applications.clear()
        return applications
    except json.JSONDecodeError as error:
        raise ValueError(
            "Application file contains invalid JSON."
        ) from error

    if not isinstance(loaded, dict):
        raise ValueError("Application data must be a JSON object.")

    if any(
        not isinstance(key, str) or not isinstance(value, dict)
        for key, value in loaded.items()
    ):
        raise ValueError("Application records have an invalid structure.")

    applications.clear()
    applications.update(loaded)

    return applications


def upload_to_bureau(
    report_path: str,
    user: str | None = None,
    password: str | None = None,
) -> None:
    """Upload a report securely through SFTP over SSH."""
    sftp_host = os.getenv("BUREAU_HOST")
    sftp_user = user or os.getenv("BUREAU_USER")
    sftp_password = password or os.getenv("BUREAU_PASSWORD")
    sftp_port = int(os.getenv("BUREAU_PORT", "22"))

    if not sftp_host or not sftp_user or not sftp_password:
        raise ValueError(
            "Configure BUREAU_HOST, BUREAU_USER and BUREAU_PASSWORD."
        )

    if not os.path.isfile(report_path):
        raise FileNotFoundError(report_path)

    try:
        with paramiko.SSHClient() as client:
            client.load_system_host_keys()
            client.connect(
                hostname=sftp_host,
                port=sftp_port,
                username=sftp_user,
                password=sftp_password,
                timeout=10,
            )

            with client.open_sftp() as sftp:
                remote_name = os.path.basename(report_path)
                sftp.put(report_path, remote_name)

    except (OSError, paramiko.SSHException) as error:
        raise RuntimeError(
            "SFTP upload failed. Check the server, credentials "
            "and SSH host-key configuration."
        ) from error


def notify_applicant(email: str, status: str) -> None:
    """Send an applicant notification through SMTP over TLS."""
    if not isinstance(email, str) or "@" not in email:
        raise ValueError("A valid email address is required.")

    smtp_host = os.getenv("SMTP_HOST")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_SENDER", smtp_user or "")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))

    if not all((smtp_host, smtp_user, smtp_password, sender)):
        raise ValueError(
            "Configure SMTP_HOST, SMTP_USER, SMTP_PASSWORD "
            "and SMTP_SENDER."
        )

    message = EmailMessage()
    message["Subject"] = f"Loan {status}"
    message["From"] = sender
    message["To"] = email
    message.set_content(
        f"Your loan application status is: {status}."
    )

    try:
        with smtplib.SMTP_SSL(
            smtp_host,
            port=smtp_port,
            timeout=10,
        ) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(message)

    except (OSError, smtplib.SMTPException) as error:
        raise RuntimeError(
            "Failed to send applicant notification."
        ) from error


def interest_saved(
    principal: float,
    annual_rate: float,
    years: int,
    prepayment: float,
) -> float:
    """Estimate interest saved after prepayment and re-amortisation."""
    if not is_valid_number(principal) or principal <= 0:
        raise ValueError("Principal must be greater than zero.")

    if (
        not is_valid_number(prepayment)
        or not 0 <= prepayment <= principal
    ):
        raise ValueError(
            "Prepayment must be between zero and principal."
        )

    original_emi = calculate_emi(principal, annual_rate, years)
    months = years * 12
    original_interest = original_emi * months - principal
    remaining_principal = principal - prepayment

    if remaining_principal == 0:
        return round(max(0.0, original_interest), 2)

    reduced_emi = calculate_emi(
        remaining_principal,
        annual_rate,
        years,
    )

    reduced_interest = (
        reduced_emi * months - remaining_principal
    )

    return round(
        max(0.0, original_interest - reduced_interest),
        2,
    )


def risk_band(credit_score: int) -> str:
    """Classify a valid credit score into a risk band."""
    if not is_valid_number(credit_score):
        return "INVALID"

    if not 300 <= credit_score <= 900:
        return "INVALID"

    if credit_score >= 800:
        return "LOW"

    if credit_score >= 700:
        return "MEDIUM"

    if credit_score >= 600:
        return "HIGH"

    return "VERY HIGH"


def main() -> None:
    """Run the loan calculator demonstration."""
    print(
        f"EMI for 5L at 9% for 5 years: "
        f"{calculate_emi(500000, 0.09, 5):,.2f}"
    )

    print(
        "Eligible (score 760, income 15000, EMIs 12000):",
        check_eligibility(35, 15000, 760, 12000, "personal"),
    )

    print(
        "Eligible (unknown loan type 'crypto'):",
        check_eligibility(30, 80000, 650, 0, "crypto"),
    )

    print(
        f"Max loan for income 40000: "
        f"{max_loan_amount(40000, 5000, 0.09, 5):,.2f}"
    )

    schedule = amortisation_schedule(100000, 0.12, 1)
    print("Last schedule row:", schedule[-1])

    print("Risk band for 950:", risk_band(950))

    print(
        "Interest saved by prepaying 50000:",
        interest_saved(500000, 0.09, 5, 50000),
    )

    saved_id = save_application("Anil", 500000)
    print("Saved application:", saved_id)

    loaded = load_applications()
    print("Applications on file:", len(loaded))

    print("SFTP upload and email notification skipped in demonstration.")


if __name__ == "__main__":
    main()
