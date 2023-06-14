from pprint import pprint
from main import load_timetable, _convert_time, _parse_time
from itertools import pairwise

TIMETABLE = load_timetable(r"Assignment2\timetable.txt")
TEMPLATE = "{:7}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}"


def print_draft():
    # Print Header
    print(TEMPLATE.format("", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"))
    for i in range(7, 17):
        for event in TIMETABLE:
            line = ""
            match event["day"]:
                case "mon":
                    if i == _convert_time(event["start"]) / 100:
                        line = [event["title"][:11]] + [""] * 6
                        break
                    else:
                        line = [""] * 7
                        continue
                case _:
                    line = [""] * 7

        print(TEMPLATE.format(f"{i:02d}am", *line))
        print(TEMPLATE.format(*[""] * 8))


def print_header(template: str) -> None:
    print(template.format("", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"))


def print_afterhour_event(template: str, events: list[dict[str, str]]) -> None:
    output = []
    for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
        for event in events:
            if not (event["day"] == day and _convert_time(event["start"]) <= 900):
                continue
            output.append(event["title"])
        else:
            output.append("")

    print(template.format("", *output))


def print_peak_events(template: str, events: list[dict[str, str]]) -> None:
    peak_hours = ["9am", "10am", "11am", "12am", "1pm", "2pm", "3pm", "4pm"]

    di = {day: [] for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]}

    for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
        for event in events:
            if event["day"] == day:
                di[day].append(event)

    for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
        for i, ii in pairwise(peak_hours):
            print(i)
            print(ii)
            for event in di[day]:
                if _convert_time(event["start"]) >= _convert_time(_parse_time(i)):
                    #  and _convert_time(event["end"]) <= _convert_time(_parse_time(ii)):
                    print(event["title"])
                    break


print(print_peak_events(TEMPLATE, TIMETABLE))
# slice_list = [
#     [event for event in TIMETABLE if event["day"] == day]
#     for day in ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
# ]
# # pprint(slice_list)
# print_draft()
# print()
# print_header(TEMPLATE)
# print_afterhour_event(TEMPLATE, TIMETABLE)
