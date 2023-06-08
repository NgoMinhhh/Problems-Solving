from pprint import pprint


def main():
    timetable: list[dict[str, str]] = []

    while True:
        print("==== Timetable Management ====")
        print("1. Create New Event")
        # print("2. Update Event")
        # print("3. Delete Event")
        print("4. Print Timetable")
        # print("5. Print Events on Day")
        # print("6. Save Timetable")
        print("0. Quit")
        choice = input("Enter your choice: ")
        match choice:
            case "0":
                return
            case "1":
                if event := create_event():
                    timetable.append(event)
            # case "2":
            #     if event := _find_event(prompt):
            #         new_event = create_event()
            #         event = new_event
            case "4":
                pprint(timetable)
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
        print("Invalid input! Wrong format")
        return

    # Ask time
    start = _parse_time(input("Time start (e.g. 7am, 10:30pm): "))
    if not start:
        print("Invalid input! Wrong format")
        return

    end = _parse_time(input("Time end (e.g. 7pm, 10:30am): "))
    if not end:
        print("Invalid input! Wrong format")
        return

    # Check if end time is later than start time
    if _convert_time(start) >= _convert_time(end):
        print("Invalid input! End time must be later than start time")
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


def _convert_time(time: str) -> int:
    """Convert time formatted as HH:mm am/pm into int for numeric comparison"""
    hh, mm = [t.strip() for t in time[:-2].split(":")]
    if time[-2:] == "pm" and (hh := int(hh) <= 12):
        hh += 12
    return int(f"{hh}{mm}")


def _is_available(timetable: list[dict[str, str]], new_event: dict[str, str]) -> bool:
    """Check availability by comparing start, end time of the new event against all events in the same day"""

    # Does not need to proceed if timetable is empty
    if len(timetable) == 0:
        return True

    # Get list of events in the same day and return if it is empty
    same_day_events = [e for e in timetable if e["day"] == new_event["day"]]
    if len(same_day_events) == 0:
        return True

    # Convert to comparison-enabled time format for new event
    new_start, new_end = [
        _convert_time(t) for t in (new_event["start"], new_event["end"])
    ]

    for old_event in same_day_events:
        old_start = _convert_time(old_event["start"])
        old_end = _convert_time(old_event["end"])
        # New Event cannot start or end in existing event's timeframe
        if old_start <= new_start <= old_end or old_start <= new_end <= old_end:
            return False

    return True


if __name__ == "__main__":
    main()
