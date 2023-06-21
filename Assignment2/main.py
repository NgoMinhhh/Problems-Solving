from pprint import pprint


def main():
    timetable: list[dict[str, str]] = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    while True:
        print("==== Timetable Management ====")
        print("1. Create New Event")
        print("2. Update Event")
        print("3. Delete Event")
        print("4. Print Timetable")
        print("5. Print Events on Day")
        # print("6. Save Timetable")
        print("7. Load timetable data")
        print("0. Quit")
        print("9. test")
        choice = input("Enter your choice: ")
        match choice:
            case "0":
                return
            case "1":
                if event := create_event():
                    if _is_available(timetable, event):
                        timetable.append(event)
                    else:
                        print("Event is in the timeframe of another one")
            case "2":
                update_event(timetable)
            case "3":
                # TODO: Refactor Update function
                # Ask day
                day = input("Day (e.g. monday, tue): ").lower()
                if not (_is_day(day)):
                    print("Invalid input! Wrong format")
                    return

                # Ask time
                start = _parse_time(input("Time start (e.g. 7am, 10:30pm): "))
                if not start:
                    print("Invalid input! Wrong format")
                    return
                try:
                    event = _find_events(timetable, day=day, start=start)[0]
                    confirm = input("Are you sure ? (y/n)")
                    timetable.remove(event)
                except IndexError:
                    print("No event found!")
                    return
            case "4":  # Print full timetable
                line_template = "{:5}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:9}"
                print_header(days)
                print_offwork_events(line_template, timetable, days, mode="before")
                print_working_events(line_template, timetable, days)
                print_offwork_events(line_template, timetable, days, mode="after")
            case "5":
                print_events(timetable)
            case "7":
                timetable = load_timetable(r"Assignment2\timetable copy.txt")
                if timetable:
                    print("Data load successfully!")
                else:
                    print("Load Data failed!")
            case "9":
                day = input("Day: ")
                start = _parse_time(input("Time: "))
                events = _find_events(timetable, day=day, start=start)
                _edit_field(timetable, events[0], location="s")
            case _:
                continue
        print()


def create_event() -> dict[str, str] | None:
    """Create valid event"""
    # Ask title
    if not (title := input("Title: ")):
        print("Title can not be empty!")
        return

    # Ask day
    day = input("Day (e.g. monday, tue): ")
    if not (_is_day(day)):
        print("Invalid input! Wrong format")
        return

    # Ask time
    start = _parse_time(input("Time start (e.g. 7am, 10:30pm): "))
    if not start:
        print("Invalid input! Wrong format")
        return

    end = _parse_time(input("Time end (e.g. 7pm, 10:30am): "))
    if not end:
        print("Invalid input! Wrong format")
        return

    # Check if end time is later than start time
    if _convert_time(start) >= _convert_time(end):
        print("Invalid input! End time must be later than start time")
        return

    # Ask Loc
    if location := input("Location (optional): "):
        return {
            "title": title,
            "day": day,
            "start": start,
            "end": end,
            "location": location,
        }

    # Return dict with no loc key to match interface of dict[str,str]
    return {"title": title, "day": day, "start": start, "end": end}


def _is_day(day: str) -> bool:
    """Validate day input"""
    if day.lower().strip() in [
        "monday",
        "mon",
        "tuesday",
        "tue",
        "wednesday",
        "wed",
        "thursday",
        "thu",
        "friday",
        "fri",
        "saturday",
        "sat",
        "sunday",
        "sun",
    ]:
        return True
    return False


def _parse_time(time: str) -> str:
    """Parse time in HH:mmAM/PM format, return empty string if invalid input"""
    txt = time.strip()
    try:
        # Check for AM/PM
        period = txt[-2:].lower()
        if period not in ["am", "pm"]:
            return ""

        # Get hour and minute
        match txt[:-2].split(":"):
            case (hh, mm):
                hh, mm = (hh, mm)
            case (hh,):
                hh = hh
                mm = "00"
            case _:
                return ""

        # Compare hour and minute in range
        if not (0 <= int(hh) <= 12 and 0 <= int(mm) <= 59):
            return ""

        return f"{hh.rjust(2,'0')}:{mm.rjust(2,'0')}{period}"

    except Exception:
        return ""


def _convert_time(time: str) -> int:
    """Convert time formatted as HH:mm am/pm into int for numeric comparison"""
    hh, mm = [t.strip() for t in time[:-2].split(":")]
    if time[-2:] == "pm" and (hh := int(hh)) < 12:
        hh += 12
    elif time[-2:] == "am" and int(hh) == 12:
        hh = 0
    return int(f"{hh}{mm}")


def _is_available(timetable: list[dict[str, str]], new_event: dict[str, str]) -> bool:
    """Check availability by comparing start, end time of the new event against all events in the same day"""

    # Does not need to proceed if timetable is empty
    if len(timetable) == 0:
        return True

    # Get list of events in the same day and return if it is empty
    same_day_events = [e for e in timetable if e["day"] == new_event["day"]]
    if len(same_day_events) == 0:
        return True

    # Convert to comparison-enabled time format for new event
    new_start, new_end = [
        _convert_time(t) for t in (new_event["start"], new_event["end"])
    ]

    for old_event in same_day_events:
        old_start = _convert_time(old_event["start"])
        old_end = _convert_time(old_event["end"])
        # New Event cannot start or end in existing event's timeframe
        if old_start <= new_start <= old_end or old_start <= new_end <= old_end:
            return False

    return True


def _find_events(timetable: list[dict[str, str]], **kwargs) -> list[dict[str, str]]:
    match kwargs:
        case {"day": day, "start": start, "end": end}:
            # Find all events from start-end timeframe
            # Use for printing timetable
            events = []
            cap_start, cap_end = [_convert_time(_parse_time(t)) for t in (start, end)]
            for event in timetable:
                if (
                    event["day"].lower() == day.lower()
                    and cap_start <= _convert_time(event["start"]) < cap_end
                    and _convert_time(event["end"]) <= cap_end
                ):
                    events.append(event)

        case {"day": day, "start": start}:
            # Should find one event only and return a one-item list to match interface
            # Or return an empty list
            events = [
                event
                for event in timetable
                if event["start"] == _convert_time(start) and event["day"] == day
            ]
        # case {'title': title}:
        #     ...
        # case {'location': loc}:
        #     ...
        case _:
            events = []
    return events


def update_event(timetable: list[dict[str, str]]) -> None:
    # Ask day
    day = input("Day (e.g. monday, tue): ").lower()
    if not (_is_day(day)):
        print("Invalid input! Wrong format")
        return

    # Ask time
    start = _parse_time(input("Time start (e.g. 7am, 10:30pm): "))
    if not start:
        print("Invalid input! Wrong format")
        return

    try:
        event = _find_events(timetable, day=day, start=start)[0]
    except IndexError:
        print("No event found!")
        return

    new_title = input("New Title (Skip if not change): ") or event["title"]
    new_day = input("New Day (Skip if not change): ") or event["day"]
    new_start = (
        _parse_time(input("New Time Start (Skip if not change): ")) or event["start"]
    )
    new_end = _parse_time(input("New Time End (Skip if not change): ")) or event["end"]
    new_loc = input("New Location (Skip if not change): ") or event.get("location")

    new_event = {"title": new_title, "day": new_day, "start": new_start, "end": new_end}
    if new_loc:
        new_event["location"] = new_loc

    # Remove said event from loop
    timetable.remove(event)
    if _is_available(timetable, new_event):
        timetable.append(new_event)
        print("Event updated succesfully")
    else:
        timetable.append(event)
        print("Event not updated")
    return


def _edit_field(
    timetable: list[dict[str, str]], event: dict[str, str], **kwargs
) -> dict[str, str]:
    match kwargs:
        case {"title": val}:
            event["title"] = val
            print("Title is edited")
            return {"title": val}
        case {"location": val}:
            event["location"] = val
            print("Location is edited")
            return {"location": val}
        case {"day": day}:
            new_event = event.copy()
            new_event.update(day=day)
            if _is_available(timetable, new_event):
                print("Day is edited")
                event["day"] = day
                return {"day": day}
            else:
                print("There is another event scheduled in the same timeframe!")
                choice = input("Do you want to update new time (y/n)? ").lower()
                if choice != "y":
                    return _edit_field(timetable, event, day=day, start=None, end=None)
        case {
            "day": day,
        }:
            ...


def load_timetable(filename: str) -> list[dict[str, str]]:
    """Load timetable from txt file and return empty list if fail"""
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        headers = lines[0].split("\t")
        tb = [
            {headers[i]: val for i, val in enumerate(line.split("\t"))}
            for line in lines[1:]
        ]
    return tb


def save_timetable(timetable: list[dict[str, str]], filename: str) -> None:
    """Save timetable into txt file, separator is \, for each field"""
    with open(filename, "w", encoding="utf-8") as f:
        # Write Headers
        f.write("\,".join(timetable[0].keys()) + "\n")

        # Write data
        f.writelines(["\,".join(event.values()) + "\n" for event in timetable])


def print_events(events: list[dict[str, str]]) -> None:
    """Print events in table format"""
    print(f"Events in {events[0]['day']}:")
    print("-" * 80)
    # Print Header
    print(
        "{:^22}|{:^11}|{:^11}|{:^11}|{:^21}".format(
            "TITLE", "DAY", "START", "END", "LOCATION"
        )
    )
    print("-" * 80)
    # Print Data
    for event in events:
        print(
            "{title:22}|{day:^11}|{start:^11}|{end:^11}|{location:21}".format(
                title=event["title"],
                day=event["day"].capitalize(),
                start=event["start"],
                end=event["end"],
                location=event["location"][:20],
            )
        )

    print("-" * 80)


def print_header(days: list[str]) -> None:
    """Print Header for timetable, including an empty col for time and 7 cols for respective days"""
    print(" " * 4, "|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^9}".format(*days))
    print(("-" * 5 + ("|" + "-" * 10) * 7)[:80])


def print_offwork_events(
    line_template: str, timetable: list[dict[str, str]], days: list[str], mode: str
) -> None:
    """Print offwork events before 9am and after 5pm periods"""
    line1 = [""]
    line2 = [""]
    if mode.lower() == "before":
        start = "12am"
        end = "9am"
    elif mode.lower() == "after":
        start = "5pm"
        end = "11:59pm"
    else:
        raise ValueError("Incorrect mode")

    for day in days:
        events_2_print = _find_events(timetable, day=day, start=start, end=end)
        match len(events_2_print):
            case 0:
                line1.append("")
                line2.append("")
            case 1:
                line1.append(events_2_print[0]["title"][:9])
                line2.append(
                    f'{events_2_print[0]["start"]} - {events_2_print[0]["end"]}'[:9]
                )
            case 2:
                line1.append(events_2_print[0]["title"][:9])
                line2.append(events_2_print[1]["title"][:9])
            case _:
                line1.append(events_2_print[0]["title"][:9])
                line2.append("etc.")

    print(line_template.format(*line1))
    print(line_template.format(*line2))

    if mode == "before":
        print(("-" * 5 + ("|" + "-" * 10) * 7)[:80])


def get_multihour_events(timetable):
    multi_hour_events = []
    for event in timetable:
        # (1359 // 100 + 1) * 100)
        time_span = _convert_time(event["end"]) - _convert_time(event["start"])
        if time_span > 100:
            start_cap = _convert_time(event["start"]) // 100 * 100
            end_cap = start_cap + 100
            event["multi_timeframe"] = f"{start_cap}-{end_cap}"  # To search for
            event["border_track"] = round(time_span / 200)
            multi_hour_events.append(event)
    return multi_hour_events


def print_working_events(
    line_template: str, timetable: list[dict[str, str]], days: list[str]
) -> None:
    working_hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm"]
    multihour_events = get_multihour_events(timetable)

    for i in range(len(working_hours)):
        if i == len(working_hours) - 1:
            return
        line1 = [working_hours[i]]
        line2 = [""]
        bot_border = "-" * 5 + "|"

        for day in days:
            one_hour_events = _find_events(
                timetable, day=day, start=working_hours[i], end=working_hours[i + 1]
            )
            multihour_event = {}
            # j = len(multihour_events) - 1
            # while j < 0:
            #     if (
            #         multihour_events[i]["day"] == day
            #         and multihour_events[i]["start"] <= working_hours[i]
            #         and multihour_events[i]["end"] >= working_hours[i + 1]
            #     ):
            #         multihour_event = multihour_events[i]
            #         j = 0
            #     else:
            #         j -= 1
            # TODO: Convert break statement to while statement
            for event in multihour_events:
                start_cap, end_cap = event["multi_timeframe"].split("-")
                if (
                    event["day"].lower() == day.lower()
                    and _convert_time(_parse_time(working_hours[i])) == int(start_cap)
                    and _convert_time(_parse_time(working_hours[i + 1])) == int(end_cap)
                ):
                    multihour_event = event
                    break
            if multihour_event:
                # There is one multi hour event and will have no other events
                if multihour_event["border_track"] > 0:
                    line1.append("-" + multihour_event["title"][:9])
                    line2.append(multihour_event["location"][:9])
                    bot_border += (
                        f'{multihour_event["start"]} - {multihour_event["end"]}'[:9]
                        + ".|"
                        or " " * 10
                    )
                    multihour_event["border_track"] = 0
                    multihour_event["multi_timeframe"] = f"{end_cap}-{int(end_cap)+100}"
                else:
                    line1.append("")
                    line2.append("")
                    bot_border += "-" * 10 + "|"
            elif len(one_hour_events) == 1:
                # There is one event in this timeframe
                line1.append("-" + one_hour_events[0]["title"][:9])
                line2.append("-" + one_hour_events[0]["location"][:9])
                bot_border += "-" * 10 + "|"
            elif len(one_hour_events) == 2:
                # There are more than 2 events scheduled in this timeframe
                line1.append("-" + one_hour_events[0]["title"][:9])
                line2.append("-" + one_hour_events[1]["title"][:9])
                bot_border += "-" * 10 + "|"
            else:
                line1.append("")
                line2.append("")
                bot_border += "-" * 10 + "|"

        # Print all output line
        print(line_template.format(*line1)[:80])
        print(line_template.format(*line2)[:80])
        print(bot_border[:80])


if __name__ == "__main__":
    main()
