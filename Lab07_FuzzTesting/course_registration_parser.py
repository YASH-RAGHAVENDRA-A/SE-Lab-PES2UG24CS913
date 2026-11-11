
def format_course_code(code):
    """
    Formats a course code safely.
    Example: cs 301 -> CS301
    """
    if not isinstance(code, str):
        return ""

    parts = code.strip().split()

    if len(parts) != 2:
        return ""

    dept, number = parts

    if not dept.isalpha() or not number.isdigit():
        return ""

    return dept.upper() + number



def total_credits(text):
    """
    Calculates total credits from comma-separated values.
    Returns 0 for invalid input.
    """
    if not isinstance(text, str) or not text.strip():
        return 0

    values = text.split(",")
    credits = []

    for value in values:
        value = value.strip()

        if not value.isdecimal():
            return 0

        try:
            credits.append(int(value))
        except (ValueError, OverflowError):
            return 0

    return sum(credits)



def parse_student_record(line):
    """
    Parses SRN|name|status safely.
    """
    empty_record = {
        "srn": "",
        "name": "",
        "status": ""
    }

    if not isinstance(line, str):
        return empty_record

    parts = line.split("|")

    if len(parts) != 3:
        return empty_record

    srn, name, status = [part.strip() for part in parts]

    if not srn or not name or not status:
        return empty_record

    return {
        "srn": srn.upper(),
        "name": name,
        "status": status.lower()
    }


def main():
    print("==== Running format_course_code ====")

    code = input("Enter course code: ")
    print("Formatted course code:", format_course_code(code))

    print("\n==== Running total_credits ====")

    credits = input("Enter credits separated by commas: ")
    print("Total credits:", total_credits(credits))

    print("\n==== Running parse_student_record ====")

    record = input("Enter SRN|name|status: ")
    print("Student record:", parse_student_record(record))


if __name__ == "__main__":
    main()
