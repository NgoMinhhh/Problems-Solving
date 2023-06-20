import main


def test_parse_time():
    di = {"7am": "07:00am", "8:30Pm": "08:30pm", "11:3am": "11:03am"}

    new_di = {t: main._parse_time(t) for t in di.keys()}
    assert di == new_di


di = [
    ["Gym", "mon", "7:00am", "7:30am", ""],
    ["DS Seminar", "mon", "10:00am", "11:00am", "F1-24"],
    ["Tutoring", "mon", "7:00pm", "8:30pm", ""],
    ["Gym", "tue", "7:00am", "7:30am", ""],
    ["CS Lecture", "tue", "1:10pm", "3:00pm", "Online"],
    ["CS Practical", "tue", "3:10pm", "4:00pm", "P1-13"],
    ["Gym", "wed", "7:00am", "7:30am", ""],
    ["DS Practical", "wed", "11:10am", "12:00pm", "P1-13"],
    ["Tutoring", "wed", "7:00pm", "8:30pm", ""],
    ["Gym", "thu", "7:00am", "7:30am", ""],
    ["Lunch with Kevin", "thu", "12:00pm", "1:00pm", ""],
    ["Gym", "fri", "7:00am", "7:30am", ""],
    ["Meet Project Manager", "fri", "10:00am", "10:30am", ""],
    ["Meet Supervisor", "fri", "10:30am", "11:00am", ""],
    ["Book Club", "fri", "2:30pm", "4:00pm", "MLK Library"],
]
with open(r"Assignment2\timetable copy.txt", "w") as f:
    f.write("\t".join(["title", "day", "start", "end", "location"]) + "\n")
    for e in di:
        f.write("\t".join(t for t in e) + "\n")
with open(r"Assignment2\timetable copy.txt", "r") as f:
    for line in f.readlines():
        print(line.split("\t"))

# def test_is_available():
#     event1 = {"title": "1234", "day": "mon", "start": "07:00AM", "end": "07:30AM"}
#     event2 = {"title": "1234", "day": "mon", "start": "07:45AM", "end": "08:30AM"}
#     tb = main.load_main(r"Assignment2/main.txt")
#     assert main._is_available(tb, event1) == False
#     assert main._is_available(tb, event2) == False
