def main():
    timetable : list[dict[str,str]] = []

    while True:
        print("==== Timetable Management ====")
        print("1. Create Event")
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
                create_event(timetable)
            case _:
                continue
        print()

def create_event(timetable: list[dict[str,str]]) -> None:
    """Create valid event"""
    # Ask title
    if not(title := input("Title: ")):
        print("Title can not be empty!")
        return
    
    # Ask Loc
    location = input("Location (optional): ")

    # Ask day & time
    day = input("Day (e.g. monday, tue): ")
    start = input("Time start (e.g. 7am, 10:30pm): ")
    end = input("Time end (e.g. 7pm, 10:30am): ")

if __name__ == '__main__':
    main()