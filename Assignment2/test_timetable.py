import main


def test_parse_time():
    di = {"7am": "07:00am", "8:30Pm": "08:30pm", "11:3am": "11:03am"}

    new_di = {t: main._parse_time(t) for t in di.keys()}
    assert di == new_di


# def test_is_available():
#     event1 = {"title": "1234", "day": "mon", "start": "07:00AM", "end": "07:30AM"}
#     event2 = {"title": "1234", "day": "mon", "start": "07:45AM", "end": "08:30AM"}
#     tb = main.load_main(r"Assignment2/main.txt")
#     assert main._is_available(tb, event1) == False
#     assert main._is_available(tb, event2) == False
