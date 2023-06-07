import timetable


def test_parse_time():
    txt = timetable._parse_time("7:00am")
    assert txt == "07:00am"

    txt = timetable._parse_time("7am")
    assert txt == "07:00am"

def test_is_available():
    event1 = {'title':'1234','day':'mon','start':'07:00AM','end':'07:30AM'}
    event2 = {'title':'1234','day':'mon','start':'07:45AM','end':'08:30AM'}
    tb = timetable.load_timetable(r'Assignment2/timetable.txt')
    assert timetable._is_available(tb,event1) == False
    assert timetable._is_available(tb,event2) == False
