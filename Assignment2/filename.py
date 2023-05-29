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
    pprint(timetable)


def display_title():
    """Display author info and program title"""
    print("Author: Nhat Minh Ngo")
    print("Email ID: ngony007")
    print("WEEKLY TIMETABLE")


def get_choice() -> int:
    """Display menu for user"""
    options = [
        "Quit",
        "Create new event",
        "Update event",
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
    day = _ask_day()
    start = input("Start: ")
    end = input("End: ")

    # timetable.append(event)  # type: ignore

def _parse_time(txt) -> str:
    # TODO: split string by ; and try looking for AM/PM, convert hour and minute to int and compare in range
    pass

def _ask_start() -> str:
    while True:
        start = input("Start: ")
        if 

def _ask_day() -> str:
    while True:
        day = input("Day: ")
        if _validate_day(day):
            return day


def _validate_day(txt: str) -> bool:
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
        day = input("Day ?")
        if not timetable.get(day):
            continue
        start = input("Start time ?")
        for event in timetable[day]:
            if event["Start"] == start:
                return event
        else:
            return None


def edit_event(timetable: dict[str, list[dict[str, str]]]):
    """Edit existing event, prompt user for start time"""
    event = _find_event(timetable)
    if not event:
        print
    while True:
        choice = input(
            "Select field to edit: Title, Day, Start time, End time, location or quit?"
        )
    pass


def print_timetable(timetable):
    pass


def _check_availability(day: str, start: str, end: str) -> bool:
    """Check event against existing timetable"""
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
                timetable.append({headers[i]: data[i] for i in range(len(data))})
    except FileNotFoundError:
        return []
    return timetable


main()
