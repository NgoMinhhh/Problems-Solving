#
# File: filename.py
# Author: Nhat Minh Ngo
# Student ID: 110401845
# Email ID: ngony007
# This is my own work as defined by
#   the University's Academic Misconduct Policy.

timetable_struct = {
    "mon": [{"Title": "Gym", "Start": "07:00am", "End": "10:30am"}],
    "tue": [],
    "wed": [],
    "thu": [],
    "fri": [],
    "sat": [],
    "sun": [],
}


def main():
    print("Author: Nhat Minh Ngo\nEmail ID: ngony007")

    timetable = load_timetable("timetable.txt")
    # command = ""
    # while command != "q" or command != "quit":
    #     command = input()


def load_timetable(filename: str) -> dict[str, list[dict[str, str]]]:
    
    try: 
        with open(filename, 'r') as f:
            


main()
