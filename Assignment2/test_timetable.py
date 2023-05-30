import timetable


def test_parse_time():
    txt = timetable._parse_time("7:00am")
    assert txt == "07:00am"

    txt = timetable._parse_time("7am")
    assert txt == "07:00am"
