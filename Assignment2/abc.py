from pprint import pprint
from main import load_timetable, _convert_time, _parse_time, _find_events
from itertools import pairwise

TIMETABLE = load_timetable(r"Assignment2\timetable copy.txt")
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


def print_offwork_events(
    template: str, events: list[dict[str, str]], mode: str
) -> None:
    line1 = [""]
    line2 = [""]
    if mode.lower() == "before":
        start = "12am"
        end = "9am"
    elif mode.lower() == "after":
        start = "5pm"
        end = "12am"
    else:
        raise ValueError("Incorrect mode")

    for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
        events_2_print = _find_events(timetable=events, day=day, start=start, end=end)
        match len(events_2_print):
            case 0:
                line1.append("")
                line2.append("")
            case 1:
                line1.append(events_2_print[0]["title"])
                line2.append(f'events_2_print[0]["start"] - events_2_print[0]["end"]')
            case 2:
                line1.append(events_2_print[0]["title"])
                line2.append(events_2_print[1]["title"])
            case _:
                line1.append(events_2_print[0]["title"])
                line2.append("etc.")

    print(template.format(*line1))
    print(template.format(*line2))

    if mode == "before":
        print("-" * 80)


def triplewise(iterable):
    "Return overlapping triplets from an iterable"
    # triplewise('ABCDEFG') --> ABC BCD CDE DEF EFG
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def print_peak_events(template: str, events: list[dict[str, str]]) -> None:
    peak_hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm"]
    multihour_events = get_multihour_events(events)

    for i, ii in pairwise(peak_hours):
        line1 = [i]
        line2 = [""]
        bot_border = "-" * 6
        for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
            # Check if there is any event in the same timeframe of 1 hour
            one_hour_events = _find_events(events, day=day, start=i, end=ii)
            # two_hour_events = _find_events(
            #     events, day=day, start=i, end=ii, is_inclusive=True
            # )
            multihour_event = None
            for event in multihour_events:
                if event["day"] == day and event["start"] <= i and event["end"] >= ii:
                    multihour_event = event
                    break

            if multihour_event:
                if multihour_event["border_track"] > 0:
                    line1.append("-" + multihour_event["title"][:9])
                    line2.append(
                        f"{_convert_time_display(multihour_event['start'])[:-2]}-{_convert_time_display(multihour_event['end'])}"
                    )
                    multihour_event["border_track"] = 0
                else:
                    line1.append("")
                    line2.append("")
                bot_border += " " * 10
            elif len(one_hour_events) == 1:
                # There is only one event in this timeframe
                line1.append("-" + one_hour_events[0]["title"][:9])
                line2.append("at " + one_hour_events[0]["location"][:7])
                bot_border += "-" * 11
            elif len(one_hour_events) == 2:
                # There are more than 2 events scheduled in this timeframe
                line1.append("-" + one_hour_events[0]["title"][:9])
                line2.append("-" + one_hour_events[1]["title"][:9])
                bot_border += "-" * 11
            else:
                line1.append("")
                line2.append("")
                bot_border += "-" * 11

        # Print all output line
        print(template.format(*line1)[:80])
        print(template.format(*line2)[:80])
        print(bot_border[:80])


def get_multihour_events(TIMETABLE):
    multi_hour_events = []
    for event in TIMETABLE:
        time_span = _convert_time(event["end"]) - _convert_time(event["start"])
        if time_span > 100:
            event["border_track"] = round(time_span / 200)
            multi_hour_events.append(event)
    return multi_hour_events


def _convert_time_display(time: str) -> str:
    hh, mm = [t.strip() for t in time[:-2].split(":")]
    period = time[-2:].lower()
    if int(mm) == 0:
        return f"{int(hh)}{period}"
    else:
        return f"{int(hh)}:{mm}{period}"


print_header()
print_offwork_events(TEMPLATE, TIMETABLE, mode="before")
print_peak_events(TEMPLATE, TIMETABLE)
print_offwork_events(TEMPLATE, TIMETABLE, mode="after")


# print(TEMPLATE.format(*[""] * 8))
# print(TEMPLATE.format(*[""] * 8))
# print("-" * 6, " " * 8, "-" * 64)
# print(TEMPLATE.format(*[""] * 8))
# print(TEMPLATE.format(*[""] * 8))
# print("-" * 80)
# print(TEMPLATE.format(*[""] * 8))
# print(TEMPLATE.format(*[""] * 8))
# print("-" * 17, " " * 8, "-" * 53)
# print(TEMPLATE.format(*[""] * 8))
# print(TEMPLATE.format(*[""] * 8))
# print("-" * 28, " " * 8, "-" * 42)
# print(TEMPLATE.format(*[""] * 8))
# print(TEMPLATE.format(*[""] * 8))
# print("-" * 39, " " * 8, "-" * 31)
# print(TEMPLATE.format(*[""] * 8))
# print(TEMPLATE.format(*[""] * 8))
# print("-" * 50, " " * 8, "-" * 20)
# print(TEMPLATE.format(*[""] * 8))
# print(TEMPLATE.format(*[""] * 8))
# print("-" * 61, " " * 8, "-" * 9)
# print(TEMPLATE.format(*[""] * 8))
# print(TEMPLATE.format(*[""] * 8))
# print("-" * 72, " " * 8)
# print(TEMPLATE.format(*[""] * 8))
# print(TEMPLATE.format(*[""] * 8))
# print("-" * 80)
