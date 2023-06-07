def main():
    timetable : list[dict[str,str]] = []

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
            case '0':
                return
            case '1':
                create_event()
            case _:
                continue
        print()

def create_event() -> dict[str,str] | None:
    """Create valid event"""
    # Ask title
    if not(title := input("Title: ")):
        print("Title can not be empty!")
        return

    # Ask day
    day = input("Day (e.g. monday, tue): ")
    if not(_is_day(day)):
        print('Day is not valid')
        return
    
    # Ask time
    start = input("Time start (e.g. 7am, 10:30pm): ")
    end = input("Time end (e.g. 7pm, 10:30am): ")

    # Ask Loc
    if location := input("Location (optional): "):
        return {'title':title,'day':day,'start':start,'end':end,'location':location}
    
    # Return dict with no loc key to match interface of dict[str,str]
    return {'title':title,'day':day,'start':start,'end':end}

def _is_day(day:str) -> bool:
    """Validate day input"""
    if day.lower().strip() in ["monday",
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
        "sun"]:
        return True
    return False

def _parse_time(time:str) -> str:
    pass
if __name__ == '__main__':
    main()