from pprint import pprint


def main():
    timetable: list[dict[str, str]] = []

    while True:
        print("==== Timetable Management ====")
        print("1. Create New Event")
        print("2. Update Event")
        # print("3. Delete Event")
        print("4. Print Timetable")
        print("5. Print Events on Day")
        # print("6. Save Timetable")
        print("7. Load timetable data")
        print("0. Quit")
        print("9. test")
        choice = input("Enter your choice: ")
        match choice:
            case "0":
                return
            case "1":
                if event := create_event():
                    if _is_available(timetable, event):
                        timetable.append(event)
                    else:
                        print("Event is in the timeframe of another one")
            case "2":
                update_event(timetable)
            case "4":
                pprint(timetable)
            case "5":
                print_events(timetable)
            case "7":
                timetable = load_timetable(r"Assignment2\timetable.txt")
                if timetable:
                    print("Data load successfully!")
                else:
                    print("Load Data failed!")
            case "9":
                day = input("Day: ")
                start = _parse_time(input("Time: "))
                events = _find_events(timetable, day=day, start=start)
                _edit_field(timetable, events[0], location="s")
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


def _find_events(timetable: list[dict[str, str]], **kwargs) -> list[dict[str, str]]:
    match kwargs:
        case {"day": day, "start": start}:
            # Should find one event only and return a one-item list to match interface
            # Or return an empty list
            events = [
                event
                for event in timetable
                if event["start"] == start and event["day"] == day
            ]
        # case {'title': title}:
        #     ...
        # case {'location': loc}:
        #     ...
        case _:
            events = []
    return events


def update_event(timetable: list[dict[str, str]]) -> None:
    # Ask day
    day = input("Day (e.g. monday, tue): ").lower()
    if not (_is_day(day)):
        print("Invalid input! Wrong format")
        return

    # Ask time
    start = _parse_time(input("Time start (e.g. 7am, 10:30pm): "))
    if not start:
        print("Invalid input! Wrong format")
        return

    try:
        event = _find_events(timetable, day=day, start=start)[0]
        timetable.remove(event)
    except IndexError:
        print("No event found!")
        return

    new_title = input("New Title (Skip if not change): ") or event["title"]
    new_day = input("New Day (Skip if not change): ") or event["day"]
    new_start = (
        _parse_time(input("New Time Start (Skip if not change): ")) or event["start"]
    )
    new_end = _parse_time(input("New Time End (Skip if not change): ")) or event["end"]
    new_loc = input("New Location (Skip if not change): ") or event.get("location")

    new_event = {"title": new_title, "day": new_day, "start": new_start, "end": new_end}
    if new_loc:
        new_event["location"] = new_loc

    if _is_available(timetable, new_event):
        timetable.append(new_event)
        print("Event updated succesfully")
    else:
        timetable.append(event)
        print("Event not updated")
    return


def _edit_field(
    timetable: list[dict[str, str]], event: dict[str, str], **kwargs
) -> dict[str, str]:
    match kwargs:
        case {"title": val}:
            event["title"] = val
            print("Title is edited")
            return {"title": val}
        case {"location": val}:
            event["location"] = val
            print("Location is edited")
            return {"location": val}
        case {"day": day}:
            new_event = event.copy()
            new_event.update(day=day)
            if _is_available(timetable, new_event):
                print("Day is edited")
                event["day"] = day
                return {"day": day}
            else:
                print("There is another event scheduled in the same timeframe!")
                choice = input("Do you want to update new time (y/n)? ").lower()
                if choice != "y":
                    return _edit_field(timetable, event, day=day, start=None, end=None)
        case {
            "day": day,
        }:
            ...


def load_timetable(filename: str) -> list[dict[str, str]]:
    """Load timetable from txt file and return empty list if fail"""
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        headers = lines[0].split("\,")
        tb = [
            {headers[i]: val for i, val in enumerate(line.split("\,"))}
            for line in lines[1:]
        ]
    return tb


def save_timetable(timetable: list[dict[str, str]], filename: str) -> None:
    """Save timetable into txt file, separator is \, for each field"""
    with open(filename, "w", encoding="utf-8") as f:
        # Write Headers
        f.write("\,".join(timetable[0].keys()) + "\n")

        # Write data
        f.writelines(["\,".join(event.values()) + "\n" for event in timetable])


def print_events(events: list[dict[str, str]]) -> None:
    """Print events in table format"""
    print(f"Events in {events[0]['day']}:")
    print("-" * 79)
    # Print Header
    print(
        "|{:^20}|{:^11}|{:^11}|{:^11}|{:^20}|".format(
            "TITLE", "DAY", "START", "END", "LOCATION"
        )
    )
    print("-" * 79)
    # Print Data
    for event in events:
        print(
            "|{title:20}|{day:^11}|{start:^11}|{end:^11}|{location:20}|".format(
                title=event["title"],
                day=event["day"].capitalize(),
                start=event["start"],
                end=event["end"],
                location=event["location"][:20],
            )
        )

    print("-" * 79)


if __name__ == "__main__":
    main()
