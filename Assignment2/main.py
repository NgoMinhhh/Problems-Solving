# File: main.py
# Author: Nhat Minh Ngo
# Student ID: 110401845
# Email ID: ngony007
# This is my own work as defined by
#   the University's Academic Misconduct Policy.

# TODO: write display function


def main():
    # Display Author info
    print("Author: Nhat Minh Ngo")
    print("Email : ngony007@mymail.unisa.edu.au")

    # Initialize 'global' variables
    timetable: list[dict[str, str]] = []
    ## Default display days in timetable, can be changed via option 8
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Primary loop for menu
    while True:
        print(f"{' TIMETABLE MANAGEMENT ':=^80}")
        options: list[str] = [
            "0. Quit",
            "1. Create Event",
            "2. Update Event",
            "3. Delete Event",
            "4. Find Events",
            "5. Display Timetable",
            "6. Export Timetable",
            "7. Import Timetable",
            "8. Set Week Start day",
        ]
        # To display options in two cols style
        # Left col for odd numbered, right col for even numbered options
        for i in range(len(options)):
            try:
                if i % 2 == 0:
                    print("{:40}{:40}".format(options[i], options[i + 1]))
                else:
                    continue
            except IndexError:
                print("{:40}{:40}".format(options[i], ""))
        print("-" * 80)
        # Ask for Choice
        menu_choice = input(" - Enter your choice: ")
        # Match-Case instead of If-else for cleaner branching
        match menu_choice:
            case "0":  # Quit Program
                if ask_confirmation("You are about to QUIT program."):
                    return
                continue
            case "1":  # Create New Event
                # Ask for all info to create a event
                print("=> Input info for new event")
                try:
                    event = ask_info(
                        {
                            "title": " - Title (Required) : ",
                            "location": " - Location (Optional): ",
                            "day": " - Day: ",
                            "start": " - Start (e.g. 7am, 10:30pm): ",
                            "end": " - End (e.g. 7am, 10:30pm): ",
                        }
                    )
                except Exception as e:
                    print(e)
                    continue

                # Check new event for availibility
                if is_available(timetable, event):
                    if ask_confirmation("~You are ADDING new event~"):
                        timetable.append(event)
                        print("RESULT: Event created successfully")
                    else:
                        print("RESULT: Action aborted")
                else:
                    print("ERROR! Event is in the timeframe of another one")
            case "2" | "3" | "4":  # Update Event / Delete Event / Find Events
                # Ask user for method to search for events
                print("=> Select Search Options")
                search_options = [
                    "Day and Start Time",
                    "Day Only",
                    "Title",
                    "Location",
                ]
                print(
                    "\n".join(
                        [
                            f" {i}. {search_options[i]}"
                            for i in range(len(search_options))
                        ]
                    )
                )

                # Process user choice. Should choice be invalid, return to menu
                search_choice = input(" - Enter your choie: ")
                try:
                    match search_choice:
                        case "0":  # Day and Start will result in exactly 1 event or none at all
                            search_terms = ask_info(
                                {"day": "Day: ", "start": "Start time: "}
                            )
                        case "1" | "2" | "3":  # other options will return more than 1 events or none at all
                            search_field = search_options[int(search_choice)].split(
                                " "
                            )[0]
                            search_terms = ask_info(
                                {search_field.lower(): f" - {search_field}: "}
                            )
                        case _:
                            print("ERROR! Invalid choice")
                            continue
                except Exception as e:
                    print(e)
                    continue

                # Find Events that match selected criterion
                events = _find_events(timetable, **search_terms)
                if not events:
                    print("RESULT: No event found")
                    continue

                # Print out found events
                sort_timetable(timetable, days)
                print_events(events)

                # Finish Find Events. Continue for update/delete event
                if menu_choice not in ["2", "3"]:
                    continue

                # Ask user for event ID to update/delete
                tries = True
                while tries:
                    try:
                        event_id = int(input("Choose Event ID: "))
                        old_event = events[event_id]
                        tries = False
                    except (IndexError, ValueError):
                        print("ERROR! Invalid choice. Please choose again")

                if menu_choice == "3":  # Delete Event
                    if ask_confirmation("~You are DELETING event~"):
                        timetable.remove(old_event)
                        print("RESULT: Event deleted successfully")
                    else:
                        print("RESULT: Action aborted")
                    continue
                elif menu_choice == "2":  # Update Event
                    # Delete chosen event anyway to run loop checking availability
                    timetable.remove(old_event)

                # Get user input for new event
                tries = True
                while tries:
                    print("### Input new info. Skip if not change")
                    new_event = ask_info(
                        {
                            "title": " - New Title: ",
                            "day": " - New Day: ",
                            "start": " - New Time Start: ",
                            "end": " - New Time End: ",
                            "location": " - New Location: ",
                        },
                        allow_blank=True,
                    )
                    # Merge changes
                    new_event = {
                        k: v if v else old_event[k] for k, v in new_event.items()
                    }
                    if is_available(timetable, new_event):
                        if ask_confirmation("~You are UPDATING event~"):
                            timetable.append(new_event)
                            print("RESULT: Event updated successfully")
                        else:
                            timetable.append(old_event)
                            print("RESULT: Action aborted")
                        tries = False
                    else:
                        print("ERROR! Event is in the timeframe of another one")
            case "5":  # Print full timetable
                line_template = "{:5}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:9}"
                print(f"{'TIMETABLE':=^80}")
                print_tb_header(days)
                print_tb_offworks(line_template, timetable, days, mode="before")
                print_tb_working(line_template, timetable, days)
                print_tb_offworks(line_template, timetable, days, mode="after")
            case "6":  # TODO: Export Timetable
                pass
            case "7":  # Import Timetable
                print("=> Load Timetable data")
                filename = input(" - Filename: ")
                try:
                    staging_tb = load_timetable(filename)
                except Exception as e:
                    print(e)
                    continue
                # Check validity of save file
                if _is_valid(staging_tb):
                    if ask_confirmation(
                        """~You are IMPORTING new timetable~\n
                        ## This action will overwrite existing timetable~"""
                    ):
                        timetable = staging_tb
                        sort_timetable(timetable, days)
                        print("RESULT: Data load successfully!")
                    else:
                        print("RESULT: Action aborted")
                else:
                    print("ERROR: Timetable data is not valid")
            case "8":  # Change Week start day
                print("=> Change Week Start")
                print(f"## Current Week Start day is {days[0].upper()}DAY")
                print(
                    f"0. Cancel\n1. Change to {'Monday' if days[0]== 'Sun' else 'Sunday'}"
                )
                change_choice = input(" - Enter your choice: ")
                if change_choice == "1":
                    if ask_confirmation("~You are CHANGING Week Start Day~"):
                        if days[0] == "Mon":
                            days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
                        else:
                            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                elif change_choice != "0":
                    print("ERROR! Invalid Choice")
            case _:
                print("ERROR! Invalid Choice. Please select again!")
                continue
        print()


def _is_valid(staging_tb: list[dict[str, str]]) -> bool:
    """Check validity of imported timetable"""
    temp_tb = []
    for temp_event in staging_tb:
        if is_available(temp_tb, temp_event):
            temp_tb.append(temp_event)
        else:
            return False
    else:
        return True


def ask_info(fields: dict[str, str], allow_blank: bool = False) -> dict[str, str]:
    """Encapsulation for all ask for input and validation features
    ### Params
    1. fields:
        - key: for field(title, loc, day, etc)
        - value: prompt for input
    2. allow_blank:
        - flag allowing blank for values
        - location can always be blank regardless
    ### Return
    Dict with key as field name and value as input
    ### Raise
    ValueError if violating any validation
    """
    result: dict[str, str] = {}
    for field, prompt in fields.items():
        value = input(prompt)
        match field:
            case "title":
                if not value and not allow_blank:
                    raise ValueError(f"ERROR! Title must not be blank!")
            case "location":
                pass
            case "day":
                valid_days = (
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
                )
                value = value.lower()
                if value not in valid_days and not allow_blank:
                    raise ValueError("ERROR! Only accept full day or first 3 letters")
            case "start" | "end":
                if not value and not allow_blank:
                    raise ValueError(f"ERROR! {field.capitalize()} must not be blank!")
                elif not value and allow_blank:
                    pass
                else:
                    try:
                        value = parse_time(value)
                    except Exception as e:
                        raise e

        result[field] = value

    # Check if end time is later than start time
    if result.get("start") and result.get("end"):
        if _convert_time(result["start"]) > _convert_time(result["end"]):
            raise ValueError("ERROR! End time must be later than start time")
    return result


# No need for this func
# TODO: refactor it to main again
def ask_search_terms() -> dict[str, str]:
    """Use for finding events"""
    print(" a. Day and Start time")
    print(" b. Day only")
    print(" c. Title")
    print(" d. Location")
    choice = input(" - Enter your choice: ")
    try:
        match choice:
            case "a":
                search_term = ask_info({"day": "Day: ", "start": "Start: "})
            case "a":
                search_term = ask_info({"day": "Day: "})
            case "c":
                search_term = ask_info({"title": "Title: "})
            case "d":
                search_term = ask_info({"location": "Location: "})
            case _:
                raise ValueError("ERROR! Invalid Choice")
    except Exception as e:
        raise e

    return search_term


def parse_time(time: str) -> str:
    """Parse time to HH:mmAM/PM format"""
    txt = time.strip()
    # Check for AM/PM
    period = txt[-2:].lower()
    if period not in ["am", "pm"]:
        raise ValueError("ERROR! TIME must have am or pm")

    # Get hour and minute
    match txt[:-2].split(":"):
        case (hh, mm):
            hh, mm = (hh, mm)
        case (hh,):
            hh = hh
            mm = "00"
        case _:
            raise ValueError("ERROR! Time not in HH:mm format")

    # Compare hour and minute in range
    if not (0 < int(hh) <= 12 and 0 <= int(mm) <= 59):
        raise ValueError("ERROR! Hour or Minute not in valid range")

    # example return value: 7:00am, 10:15pm
    return f"{hh}:{mm.rjust(2,'0')}{period}"


def _convert_time(time: str) -> int:
    """Convert time formatted as HH:mm am/pm into int for numeric comparison"""
    try:
        hh, mm = [t.strip() for t in time[:-2].split(":")]
        if time[-2:] == "pm" and (hh := int(hh)) < 12:
            hh += 12
        elif time[-2:] == "am" and int(hh) == 12:
            hh = 0
        return int(f"{hh}{mm}")
    except (ValueError, IndexError):
        raise ValueError("ERROR! Time not in HH:mm format")


def is_available(timetable: list[dict[str, str]], new_event: dict[str, str]) -> bool:
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
        if old_start < new_start < old_end or old_start < new_end < old_end:
            return False

    return True


def _find_events(timetable: list[dict[str, str]], **kwargs) -> list[dict[str, str]]:
    match kwargs:
        case {"day": day, "start": start, "end": end}:
            # Find all events from start-end timeframe
            # Use for printing timetable
            events = []
            cap_start, cap_end = [_convert_time(parse_time(t)) for t in (start, end)]
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
                if event["start"] == _convert_time(parse_time(start))
                and event["day"].lower() == day.lower()
            ]
        case {"day": val}:
            events = [
                event for event in timetable if val.lower() in event["day"].lower()
            ]
        case {"title": val}:
            events = [
                event for event in timetable if val.lower() in event["title"].lower()
            ]
        case {"location": val}:
            events = [
                event for event in timetable if val.lower() in event["location"].lower()
            ]
        case _:
            events = []
    return events


def load_timetable(filename: str) -> list[dict[str, str]]:
    """Load timetable from txt file"""
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
            headers = lines[0].split("\t")
            tb: list[dict[str, str]] = []
            for line in lines[1:]:
                event: dict[str, str] = {}
                event_data = line.split("\t")
                for i in range(len(event_data)):
                    event[headers[i]] = event_data[i]
                tb.append(event)
        return tb
    except FileNotFoundError:
        raise FileNotFoundError("ERROR! File cannot be found")
    except LookupError:
        raise ValueError(f"ERROR! Cannot load line {i+1}")


def save_timetable(timetable: list[dict[str, str]], filename: str) -> None:
    """Save timetable into txt file, separator is \t for each field"""
    with open(filename, "w", encoding="utf-8") as f:
        headers = ("title", "day", "start", "end", "location")
        # Write Headers
        f.write("\t".join(header + "\n" for header in headers))

        # Write data only accepting values whose key match headers
        for event in timetable:
            f.write("\t".join(val for key, val in event.items() if key in headers))


def print_events(events: list[dict[str, str]]) -> None:
    """Print events in table format"""
    # Print Header
    print(
        "{:^4}|{:^24}|{:^5}|{:^9}|{:^9}|{:^24}".format(
            "ID", "TITLE", "DAY", "START", "END", "LOCATION"
        )
    )
    print("|".join(("-" * 4, "-" * 24, "-" * 5, "-" * 9, "-" * 9, "-" * 24)))
    # Print Data
    for i, event in enumerate(events):
        print(
            "{:^4}|{:24}|{:^5}|{:^9}|{:^9}|{:24}".format(
                str(i).rjust(2),
                event["title"],
                event["day"].capitalize(),
                event["start"],
                event["end"],
                event["location"],
            )
        )

    print("|".join(("-" * 4, "-" * 24, "-" * 5, "-" * 9, "-" * 9, "-" * 24)))


def print_tb_header(days: list[str]) -> None:
    """Print Header for timetable, including an empty col for time and 7 cols for respective days"""
    print(" " * 4, "|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^9}".format(*days))
    print(("-" * 5 + ("|" + "-" * 10) * 7)[:80])


def print_tb_offworks(
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
        raise ValueError("ERROR! Incorrect mode")

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
            event["border_track"] = event["max_border"] = round(time_span / 200)
            multi_hour_events.append(event)
    return multi_hour_events


def print_tb_working(
    line_template: str, timetable: list[dict[str, str]], days: list[str]
) -> None:
    work_hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm"]
    multihour_events = get_multihour_events(timetable)

    for i in range(len(work_hours)):
        if i == len(work_hours) - 1:
            return                
        line1 = [work_hours[i]]
        line2 = [""]
        bot_border = "-" * 5 + "|"

        for day in days:
            one_hour_events = _find_events(
                timetable, day=day, start=work_hours[i], end=work_hours[i + 1]
            )

            multihour_event = {}
            j = len(multihour_events) - 1
            while j >= 0:
                start_cap, end_cap = multihour_events[j]["multi_timeframe"].split("-")
                if (
                    multihour_events[j]["day"].lower() == day.lower()
                    and _convert_time(parse_time(work_hours[i])) == int(start_cap)
                    and _convert_time(parse_time(work_hours[i + 1])) == int(end_cap)
                ):
                    multihour_event = multihour_events[j]
                    j = -1
                else:
                    j -= 1

            if multihour_event:
                # There is one multi hour event and will have no other events
                if multihour_event["border_track"] == multihour_event["max_border"]:
                    line1.append("-" + multihour_event["title"][:9])
                    line2.append(multihour_event["location"][:9])
                    bot_border += (
                        f'{multihour_event["start"]} - {multihour_event["end"]}'[:9]
                        + ".|"
                        or " " * 10
                    )
                    multihour_event["border_track"] -= 1
                    multihour_event["multi_timeframe"] = f"{end_cap}-{int(end_cap)+100}"
                elif multihour_event["border_track"] == 0:
                    line1.append("")
                    line2.append("")
                    bot_border += "-" * 10 + "|"
                elif multihour_event["border_track"] < multihour_event["max_border"]:
                    line1.append("")
                    line2.append("")
                    bot_border += " " * 10 + "|"
                    multihour_event["border_track"] -= 1
                    multihour_event["multi_timeframe"] = f"{end_cap}-{int(end_cap)+100}"

            elif len(one_hour_events) == 1:
                # There is one event in this timeframe
                line1.append("-" + one_hour_events[0]["title"][:9])
                line2.append(one_hour_events[0]["location"][:9])
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


def ask_confirmation(prompt: str) -> bool:
    """Ask user for confirmation, return True/False"""
    while True:
        answer = input(f"{prompt}\n - Confirm ? (y/n): ").lower()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            continue


def sort_timetable(timetable: list[dict[str, str]], days: list[str]) -> None:
    """Sort timetable in place first with days then start time in acensding order
    ### Params
    1. timetable
    2. days: current day list"""
    ordered_days = {day.lower(): i for i, day in enumerate(days)}
    timetable.sort(
        key=lambda e: (ordered_days[e["day"].lower()], _convert_time(e["start"]))
    )


if __name__ == "__main__":
    main()
