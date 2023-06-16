from pprint import pprint
from main import load_timetable, _convert_time, _parse_time, _find_events
from itertools import pairwise

TIMETABLE = load_timetable(r"Assignment2\timetable.txt")
TEMPLATE = "{:5}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:9}"


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


def print_header() -> None:
    print(
        "{:5}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^9}".format(
            "", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
        )
    )
    print("-" * 80)


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
    peak_hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm"]

    for i, ii in pairwise(peak_hours):
        line1 = [i]
        line2 = [""]
        bot_border = "-" * 80
        for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
            # Check if there is any event in the same timeframe of 1 hour
            one_hour_events = _find_events(
                events, day=day, start=i, end=ii, is_inclusive=False
            )
            # two_hour_events = _find_events(
            #     events, day=day, start=i, end=ii, is_inclusive=True
            # )
            two_hour_events = []
            match (len(one_hour_events), len(two_hour_events)):
                case (1, 0):
                    # There is only one event in this timeframe
                    line1.append("-" + one_hour_events[0]["title"][:9])
                    line2.append("at " + one_hour_events[0]["location"][:7])
                case (2, 0):
                    # There are more than 2 events scheduled in this timeframe
                    line1.append("-" + one_hour_events[0]["title"][:9])
                    line2.append("-" + one_hour_events[1]["title"][:9])
                case (0, 0):
                    line1.append("")
                    line2.append("")

        # Print all output line
        print(template.format(*line1))
        print(template.format(*line2))
        print(bot_border)


print_header()
print_peak_events(TEMPLATE, TIMETABLE)
# slice_list = [
#     [event for event in TIMETABLE if event["day"] == day]
#     for day in ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
# ]
# # pprint(slice_list)
# print_draft()
# print()
# print_header(TEMPLATE)
# print_afterhour_event(TEMPLATE, TIMETABLE)
# pprint(
#     _find_events(
#         TIMETABLE, day="sat", start="09:00am", end="10:00am", is_inclusive=False
#     )
# )
print("\u0332".join(c for c in "123456789"))
print("\u0332".join(c for c in "123456789"))
