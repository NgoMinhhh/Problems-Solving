def main():
    timetable: list[dict[str, str]] = []

    while True:
        print("==== Timetable Management ====")
        print("1. Create New Event")
        # print("2. Update Event")
        # print("3. Delete Event")
        # print("4. Print Timetable")
        # print("5. Print Events on Day")
        # print("6. Save Timetable")
        print("0. Quit")
        choice = input("Enter your choice: ")
        match choice:
            case "0":
                return
            case "1":
                create_event()
            case _:
                continue
        print()


def create_event() -> dict[str, str] | None:
    """Create valid event"""
    # Ask title
    if not (title := input("Title: ")):
        print("Title can not be empty!")
        return

    # Ask day
    day = input("Day (e.g. monday, tue): ")
    if not (_is_day(day)):
        print("Day is not valid")
        return

    # Ask time
    start = _parse_time(input("Time start (e.g. 7am, 10:30pm): "))
    if not start:
        print("Time is not valid")
        return

    end = _parse_time(input("Time end (e.g. 7pm, 10:30am): "))
    if not end:
        print("Time is not valid")
        return

    # Ask Loc
    if location := input("Location (optional): "):
        return {
            "title": title,
            "day": day,
            "start": start,
            "end": end,
            "location": location,
        }

    # Return dict with no loc key to match interface of dict[str,str]
    return {"title": title, "day": day, "start": start, "end": end}


def _is_day(day: str) -> bool:
    """Validate day input"""
    if day.lower().strip() in [
        "monday",
        "mon",
        "tuesday",
        "tue",
        "wednesday",
        "wed",
        "thursday",
        "thu",
        "friday",
        "fri",
        "saturday",
        "sat",
        "sunday",
        "sun",
    ]:
        return True
    return False


def _parse_time(time: str) -> str:
    """Parse time in HH:mmAM/PM format, return empty string if invalid input"""
    txt = time.strip()
    try:
        # Check for AM/PM
        period = txt[-2:].lower()
        if period not in ["am", "pm"]:
            return ""

        # Get hour and minute
        match txt[:-2].split(":"):
            case (hh, mm):
                hh, mm = (hh, mm)
            case (hh,):
                hh = hh
                mm = "00"
            case _:
                return ""

        # Compare hour and minute in range
        if not (0 <= int(hh) <= 12 and 0 <= int(mm) <= 59):
            return ""

        return f"{hh.rjust(2,'0')}:{mm.rjust(2,'0')}{period}"

    except Exception:
        return ""


if __name__ == "__main__":
    main()
