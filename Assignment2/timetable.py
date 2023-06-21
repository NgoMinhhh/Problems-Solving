from pprint import pprint

#
# File: filename.py
# Author: Nhat Minh Ngo
# Student ID: 110401845
# Email ID: ngony007
# This is my own work as defined by
#   the University's Academic Misconduct Policy.

EVENT = {
    "title": "example",
    "day": "mon",
    "start": "07:00am",
    "end": "08:30pm",
    "location": "optional",
}


def main():
    display_title()

    # Load existing timetable data first
    # TODO: delete after implementing save and load functions
    timetable = load_timetable(r"Assignment2\timetable.txt")

    while True:
        choice = get_choice()
        match choice:
            case 0:
                print("Good Bye!")
                return
            case 1:
                create_event(timetable)
            case 2:
                # edit_event(timetable)
                pass
            case 4:
                pprint(timetable)
        print()


def display_title():
    """Display author info and program title"""
    print("Author: Nhat Minh Ngo")
    print("Email ID: ngony007")
    print("WEEKLY TIMETABLE MANAGER")


def get_choice() -> int:
    """Display menu for user"""
    options = [
        "Quit",
        "Create new event",
        "Edit event",
        "Delete event",
        "Print timetable",
        "Print all events in selected day",
        "Save timetable to file",
        "Load timetable from file",
        "Set start day of the week",
    ]
    print(f"Select option 0-{len(options)}")
    for i, option in enumerate(options):
        print(f" {i}. {option}")

    while True:
        choice = input("Option: ")
        try:
            if 0 <= int(choice) <= len(options):
                return int(choice)
        except TypeError | ValueError:
            continue


def create_event(timetable: list[dict[str, str]]):
    """Create new event"""
    print("Create new event")
    title = input("Title: ")
    location = input("Location (optional): ")
    day = _ask_day("Day: ")
    start = _ask_time("Start (e.g: 7:30am): ")
    end = _ask_time("End (e.g: 9:30pm): ")

    event = {"title": title, "day": day, "start": start, "end": end}
    if location:
        event["location"] = location

    if _is_available(timetable, event):
        timetable.append(event)
        print("New Event Created.")
    else:
        print("Can't Add Event")


def edit_event(timetable: dict[str, list[dict[str, str]]]):
    """Edit existing event, prompt user for start time"""
    event = _find_event(timetable)
    if not event:
        print("No event found!")
        return
    while True:
        field = input("Field to edit: ").lower()
        match field:
            case "title" | "location" as key:
                event[key] = input("New value: ")
            case "day":
                ...


def print_timetable(timetable):
    pass


def load_timetable(filename: str) -> list[dict[str, str]]:
    """Load timetable data from text file into list of dict"""
    # TODO: Escape comma in title and location field
    timetable = []
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
            headers = lines[0].split(",")
            for line in lines[1:]:
                data = line.split(",")
                timetable.append(
                    {headers[i]: data[i].lower() for i in range(len(data))}
                )
    except FileNotFoundError:
        return []
    return timetable


def _parse_time(txt: str) -> str:
    """Parse time in HH:mmAM/PM format, return empty string if invalid input"""
    txt = txt.strip()
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


def _ask_time(prompt: str) -> str:
    while True:
        if time := _parse_time(input(prompt)):
            return time


def _ask_day(prompt) -> str:
    while True:
        day = input(prompt).lower()
        if _is_day(day):
            return day


def _is_day(txt: str) -> bool:
    valid_days = [
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
    ]
    if txt in valid_days:
        return True
    return False


def _find_event(timetable) -> dict[str, str] | None:
    """Find event based on user input"""
    while True:
        day = _ask_day("Day ?")
        if not timetable.get(day):
            continue
        start = _ask_time("Start time ?")
        for event in timetable[day]:
            if event["Start"] == start:
                return event
        else:
            return None


def _is_available(timetable, event: dict[str, str]) -> bool:
    """Check day time availability against existing timetable"""
    # TODO: Convert time to 24h format and do int comparison
    if not timetable:
        return True

    new_start, new_end = [_convert_time(t) for t in (event["start"], event["end"])]
    day_events = [new_e for new_e in timetable if new_e["day"].lower() == event["day"]]
    for event in day_events:
        old_start, old_end = [_convert_time(t) for t in (event["start"], event["end"])]
        if old_start <= new_start <= old_end or old_start <= new_end <= old_end:
            return False
    return True


def _convert_time(time: str) -> int:
    hh, mm = [t.strip() for t in time[:-2].split(":")]
    if time[-2:] == "pm" and (hh := int(hh) <= 12):
        hh += 12
    return int(f"{hh}{mm}")


def do_again(func):
    """Decorator for asking back to menu or continue with chosen action"""

    def wrapper(*args, **kwargs):
        # Do action first
        func(*args, **kwargs)

        while True:
            choice = input("Option: \n0. Back to Menu\n1. Continue\n")
            if choice == "0":
                return
            elif choice == "1":
                func(*args, **kwargs)
            else:
                print("Invalid input! Please choose again.")

    return wrapper


if __name__ == "__main__":
    main()
