# File: main.py
# Author: Nhat Minh Ngo
# Student ID: 110401845
# Email ID: ngony007
# This is my own work as defined by
#   the University's Academic Misconduct Policy.


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
                events = find_events(timetable, **search_terms)
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
                # This function requires a sorted timetable
                sort_timetable(timetable, days)
                print("=> Display Timetable")
                line_template = "{:5}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:9}"
                # Print headers
                print(line_template.format("", *[day.center(10) for day in days])[:80])
                # Headers border
                print(line_template.format(*["-" * 5] + ["-" * 10] * 8)[:80])

                tb_arr = constuct_timetable_arrays(timetable, days)
                for row in tb_arr[:-1]:  # Dismiss last row as border
                    print(line_template.format(*row)[:80])
            case "6":  # Export Timetable
                print("=> Export Timetable data")
                print("## File extension is txt. Line separator is tab")
                filename = input(" - Filename: ")
                try:
                    if ask_confirmation("~You are EXPORTING timetable~"):
                        save_timetable(timetable, filename)
                        print("RESULT: Data exported successfully!")
                    else:
                        print("RESULT: Action aborted")
                except Exception as e:
                    print("ERROR!", e)
            case "7":  # Import Timetable
                print("=> Import Timetable data")
                print("## File extension must be txt. Line separator must be tab")
                filename = input(" - Filename: ")
                try:
                    staging_tb = load_timetable(filename)
                except Exception as e:
                    print(e)
                    continue
                # Check validity of save file
                if _is_valid(staging_tb):
                    if ask_confirmation(
                        """~You are IMPORTING new timetable~\n## This action will overwrite existing timetable~"""
                    ):
                        timetable = staging_tb
                        sort_timetable(timetable, days)
                        print("RESULT: Data imported successfully!")
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


def ask_confirmation(prompt: str) -> bool:
    """Init a While Loop to ask user for confirmation, only return if input is 'y' or 'n'"""
    while True:
        answer = input(f"{prompt}\n - Confirm ? (y/n): ").lower()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            continue


def ask_info(fields: dict[str, str], allow_blank: bool = False) -> dict[str, str]:
    """Encapsulation for all ask for input and validation features
    ### Params:
    1. fields:
        - key:  field(title, loc, day, etc)
        - value: prompt for input
    2. allow_blank:
        - flag allowing blank for values
        - location can always be blank regardless
    ### Return:
    Dict with key as field name and value as input
    ### Exception:
    ValueError if violating any validation
    ### Example:
    - title = ask_info('title','Input Title: ')\n
    >>> Input Title:
    >>> ValueError(f"ERROR! Title must not be blank!")\n
    - start = ask_info('start','Start Time (e.g 7am, 10:30 pm): ')\n
    >>> Start Time (e.g 7am, 10:30 pm): 7am
    >>> 7:00am\n
    - day = 'mon'
    - day = ask_info('day', 'Input day (skip if not change): ', allow_blank=True)\n
    >>> Input day (skip if not change):
    >>> 'mon'
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


def _is_valid(staging_tb: list[dict[str, str]]) -> bool:
    """Check validity of imported timetable using a 'staging' variable to run available test"""
    temp_tb = []
    for temp_event in staging_tb:
        if is_available(temp_tb, temp_event):
            temp_tb.append(temp_event)
        else:
            return False
    else:
        return True


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


def parse_time(time: str) -> str:
    """Parse time to HH:mmAM/PM format
    ### Return
    - e.g 7am -> 7:00am, 10:30PM -> 10:30pm
    ### Exception
    - Raise ValueError if invalid format"""
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


def print_events(events: list[dict[str, str]]) -> None:
    """Print events in table format\n
    ID | Title | Day | Start | End | Loc\n
    """
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
                str(i).center(4),
                event["title"],
                event["day"].capitalize(),
                event["start"],
                event["end"],
                event["location"],
            )
        )

    print("|".join(("-" * 4, "-" * 24, "-" * 5, "-" * 9, "-" * 9, "-" * 24)))


def _convert_time(time: str) -> int:
    """Convert time formatted as HH:mm am/pm into int for numeric comparison
    ### Return
    - 24h numeric
    ### Exception
    - Raise ValueError if invalid format"""
    try:
        hh, mm = [t.strip() for t in time[:-2].split(":")]
        if time[-2:] == "pm" and (hh := int(hh)) < 12:
            hh += 12
        elif time[-2:] == "am" and int(hh) == 12:
            hh = 0
        return int(f"{hh}{mm}")
    except (ValueError, IndexError):
        raise ValueError("ERROR! Time not in HH:mm format")


def find_events(timetable: list[dict[str, str]], **kwargs) -> list[dict[str, str]]:
    """Return events based on passed criterion
    ### Kwargs: pass as dictionary
    - day & start & end: Find all events from start to end
    - day & start : Find exact by day and start time (will return a one-item list if found)
    - day: Find exact by day
    - title: Find exact by title
    - location: Find exact by location
    ### Return:
    - A list of matched events or empty list if not found
    ### Example:
    - find_events(day='mon',start='7am')\n
    >>> [{'title':'gym','day':'mon','start':'7:00am','end':'8:30am'}]\n
    - find_events(title='ds')
    >>> [{'title':'DS Seminar','day':'mon','start':'10:00am','end':'11:00am','location': 'F1-24'},
        {'title':'DS Practical','day':'wed','start':'11:10am','end':'12:00pm','location': 'P1-13'}]
    """
    match kwargs:
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
    """Load timetable from tab separated text file.
    ### Exception:
    - Throw ValueError if files not found or cannot load specific line"""
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
            headers = lines[0].split("\t")  # Get Headers as keys for dict
            if len(headers) != 5:  # Check for exactly 5 fields retrieved
                raise ValueError("ERROR! File in wrong format")
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


def save_timetable(timetable: list[dict[str, str]], filename: str) -> bool:
    """Save timetable into txt file, separator is tab (\\t) for each field\n
    Will append file extension (.txt) if not input"""
    try:
        # Appending txt extension if not present in input
        if not filename.endswith(".txt"):
            filename += ".txt"
        with open(f"{filename}", "w", encoding="utf-8") as f:
            # Write Headers
            f.write("\t".join(timetable[0].keys()) + "\n")

            # Write data
            for event in timetable:
                f.write("\t".join(event.values()) + "\n")
        return True
    except Exception as e:
        raise e


def sort_timetable(timetable: list[dict[str, str]], days: list[str]) -> None:
    """Sort timetable in place first with days then start time in acensding order
    ### Params
    1. timetable
    2. days: current day list"""
    ordered_days = {day.lower(): i for i, day in enumerate(days)}
    timetable.sort(
        key=lambda e: (ordered_days[e["day"].lower()], _convert_time(e["start"]))
    )


def shorten_info(field: str, value: str, max_width: int = 9) -> str:
    """To display value in timetable"""
    match field:
        case "title" | "location":
            if len(value) > max_width:
                result = f"{value[:max_width-1]}."
            else:
                result = f"{value}"
        case "start" | "end":  # 7:00am -> 7am, 7:40am -> 7:40
            hh, mm = value[:-2].split(":")
            result = f"{int(hh)}"
            if int(mm) != 0:  # add minute if there is one
                result += f":{mm}"
            if field == "end":  # add period (am/pm) if its end time
                result += f"{value[-2:]}"
        case "time":
            start, end = value.split("-")
            result = shorten_info("start", start) + "-" + shorten_info("end", end)
        case _:
            result = ""
    return result


def constuct_timetable_arrays(
    timetable: list[dict[str, str]], days: list[str]
) -> list[list[str]]:
    """Create a 2d arrays that represents a table with row as hour and col as day. \
    row: 3 row for each timeframe, spanning 1 hour each
    col: 7 representing 7 days and 1 additional col to display hour 
    Require the timetable to be sorted first."""

    hours = ["", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", ""]
    tb_arr: list[list[str]] = []

    # An hour col with int values for hour for comparison and retrieving index from rounded time
    int_hour_col = []
    # Construct row arrays
    for hh in hours:
        row = [hh]  # each row starts with hour
        row.extend(
            [""] * len(days)
        )  # populate array with empty str which match cols number (7 days = 7 cols)
        tb_arr.append(row)
        tb_arr.append([""] * 8)  # create an empty row for each timeframe
        tb_arr.extend([["-" * 5] + ["-" * 10] * 8])  # additional row for border
        int_hour_col.extend([_convert_time(parse_time(hh)) if hh else "", "", "-"])

    # Loop through events to populate arrays
    for event in timetable:
        # Round down start and round up end time to match with row value
        rounded_start = _convert_time(event["start"]) // 100 * 100
        rounded_end = round(_convert_time(event["end"]) / 100) * 100
        # Get col index based on days list
        # +1 to account for int_hour_col
        col = days.index(event["day"].capitalize()) + 1

        if rounded_start < 900 or rounded_start > 1700:  # Before and After Work Hours
            row = 0 if rounded_start < 900 else -3  # First row or last row
            if not tb_arr[row][col]:  # There is no event
                tb_arr[row][col] = shorten_info("title", event["title"], 10)
                tb_arr[row + 1][col] = shorten_info(
                    "time", f'{event["start"]}-{event["end"]}'
                )
            elif not tb_arr[row + 1][col]:  # There is 1 event already
                tb_arr[row + 1][col] = shorten_info("title", event["title"], 10)
            else:  # More than 2 events
                tb_arr[row + 1][col] = ".etc"
        else:  # from 9am to 5pm - Work hours
            row = int_hour_col.index(rounded_start)  # match first row of timeframe
            time_span = rounded_end - rounded_start
            if time_span <= 100:  # Short event
                if not tb_arr[row][col]:  # There is no event
                    tb_arr[row][col] = shorten_info("title", event["title"], 10)
                    tb_arr[row + 1][col] = shorten_info(
                        "location", event["location"], 10
                    )
                elif not tb_arr[row + 1][col]:  # There is 1 event already
                    tb_arr[row + 1][col] = shorten_info("title", event["title"], 10)
                else:  # More than 2 events
                    tb_arr[row + 1][col] = ".etc"
            else:  # Long events (more than 1 hour)
                tb_arr[row][col] = shorten_info("title", event["title"], 10)
                tb_arr[row + 1][col] = shorten_info("location", event["location"], 10)
                tb_arr[row + 2][col] = shorten_info(
                    "time", f'{event["start"]}-{event["end"]}'
                )
                # Border delete tracker
                max_border = round((time_span) / 100) - 1
                i = 1
                while i < max_border:
                    if (border := rounded_start + i * 100) > rounded_end:
                        i = max_border
                    tb_arr[int_hour_col.index(border) + 2][col] = " " * 10
                    i += 1
                # for i in range(1,max_border):
                #     if (border:= rounded_start + i*100) > rounded_end:
                #         break
                #     tb[h_col.index(border)+2][col] = ' '*10
    return tb_arr


if __name__ == "__main__":
    main()
