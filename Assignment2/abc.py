from timetable import _convert_time, _parse_time, _is_available, load_timetable

timetable = load_timetable(r"Assignment2\timetable.txt")
while True:
    new_start = _parse_time(input("start: "))
    new_end = _parse_time(input("end: "))
    print(_is_available(timetable, input("day: "), new_start, new_end))
