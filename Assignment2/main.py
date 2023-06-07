def main():
    timetable = []

    while True:
        print("==== Timetable Management ====")
        # print("1. Create Event")
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
            case _:
                continue



if __name__ == '__main__':
    main()