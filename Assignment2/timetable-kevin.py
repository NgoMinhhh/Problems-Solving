# # File: timetable.py 
# Author: Thuan Kham To 
# Student ID: 110395039
# Email ID: toyty007 
# This is my own work as defined by  
#  the University's Academic Misconduct Policy. 
# 

def main():
    #list of events of timetable
    timetable = []
    default_days = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
    
    #print title, author's name, email
    print ("Title: Assignment 2 - Timetable")
    print("Author: Thuan Kham To")
    print("Email: toyty007@mymail.unisa.edu.au")

    #Prompt for the actionable options to manage timetable
    while True:
        print("==== Timetable Action List ====")
        print("1. Create A New Event")
        print("2. Update An Event")
        print("3. Delete An Event")
        print("4. Print Timetable")
        print("5. Find Events")
        print("6. Load Timetable")
        print("7. Save Timetable")
        print("8. Change week start day") #TODO
        print("0. Quit")
        user_choice = input("Enter your choice: ") # user choose an actionable option

        #If statement to proceed each actionable options
        if user_choice == "0":
            # Quit
            return
        elif user_choice == "1":
            # Create an event
            event = create_event()
            if not event:
                continue
            if check_available(timetable, event):
                timetable.append(event)
                print("Event created successfully")
            else:
                print("Unsuccessful! The event can't be in the timeframe of another one")
        elif user_choice == "2":
            # Update an event
            update_event(timetable)
        elif user_choice == "3": # Delete 
            # Ask for user inputs, find the event, and remove it
            print("Select from below to search for event")
            print("Press 1 for day and start time")
            print("Press 2 for title")
            print("Press 3 for location")
            search_choice = input("Your choice is ")
            if search_choice == '1':
                # Find the event or return if no event found
                day = input("Day (e.g. monday, tue): ").lower()
                if not (check_day(day)):
                    print("Invalid input due to incorrect format")
                    return

                start = input("Time start (e.g. 10:30am, 1:00pm): ").replace(" ","").lower()
                if not check_time(start):
                    print("Invalid input due to incorrect format")
                    return

                event = find_event_by_start(timetable, day, start)
                if not event:
                    print("No event found!")
                    return
            elif search_choice =='2' or search_choice == '3':
                search_val = input('Search keyword: ')
                if search_choice == '2':
                    events = find_events(timetable,'title',search_val)
                else:
                    events = find_events(timetable,'location',search_val)
                print_events(events)
                event_choice = input("Select Event ID: ")
                try:
                    event=events[int(event_choice)]
                except IndexError | TypeError:
                    print("Invalid Choice")
                    return
            else:
                print("Invalid Choice")
                return
            
            confirm = input("Are you sure ? (y/n)") # user confirmation to remove event
            if confirm =='y':
                timetable.remove(event)
                print("Event deleted Successfully")
        elif user_choice == "5": # Print selected events
            # Find an events from indicated field and value and then print
            # sort_timetable(timetable,default_days)
            field = input("Which field?: ").lower()
            value = input("What value? (first 3 letters for 'day' only): ")
            if field in ("title","day","location"):
                events = find_events(timetable, field, value) # events found from specific field and value
                print_events(events)
            else:
                print("Invalid Field")
        elif user_choice == "6":
            # Load in timetable from a file (usually ~.txt)
            filename = input("Input filename: ") # file path from user
            timetable_new = load_timetable(filename) # load new timetable from file
            if timetable_new:
                timetable = timetable_new
                # sort_timetable(timetable,default_days) 
                print("File load successfully")
            else:
                print("File load unsuccessfully")
        elif user_choice == "7":
            # Save timetable into a file
            filename = input("Input filename: ")
            sort_timetable(timetable,default_days)
            success = save_timetable(timetable, filename) # bool variable to show whether file was saved succesfully
            if success:
                print("File save successfully")
            else:
                print("File save unsuccessfully")


def create_event():
    """Create a valid event from user inputs"""
    # Ask for inputs: title, day, start, end and location
    # Validate each input for correct formatting and logic
    
    title = input("Title: ") #title of the event
    if not title:
        print("Title can not be empty!")
        return 

    #.replace() used to get rid of any space from user input
    #.lower() used to lowercase use rinput for validation
    day = input("Day (e.g. monday, tue): ").replace(" ", "").lower() # event's day happening
    if not (check_day(day)):
        print("Invalid input due to incorrect format")
        return
       
    start = input("Time start (e.g. 10:30am, 1:30pm): ").replace(" ", "").lower() # event's start time
    if not check_time(start):
        print("Invalid input due to incorrect format")
        return

    end = input("Time end (e.g. 10:30am, 1:30pm): ").replace(" ", "").lower() # event's end time
    if not check_time(end):
        print("Invalid input due to incorrect format")
        return

    # Check if end time is later than start time
    if convert_time(start) >= convert_time(end):
        print("Invalid input! End time must be later than start time!")
        return 

    location = input("Location (Optional): ") # event's location
    
    #create an event (dict) with all its key values from user inputs
    event = {
            "title": title,
            "day": day,
            "start": start,
            "end": end,
            "location": location,
        }
    return event



def check_day(day):
    """Validate day input and return T/F"""
    if day in [
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


def check_time(time):
    """Check time in HH:mmam/pm format and return T/F"""
    
    # Check for AM/PM
    period = time[-2:] # period = hold value of am or pm
    if period not in ["am", "pm"]:
        return False

    # Get hour and minute
    list_HHmm = time[:-2].split(":") # list_HHmm = list of [HH,mm]
    try:
        HH = list_HHmm[0] # HH = hour value
        mm = list_HHmm[1] # mm = minute value
    except IndexError:
        return False

    # Compare hour and minute in range
    try:
        if not (1 <= int(HH) <= 12 and 0 <= int(mm) <= 59):
            return False
    except ValueError:
        return False
    return True

    
def convert_time(time):
    """Convert time into int numeric format (eg. 12:00 am -> 2400) for comparison"""
    list_HHmm = time[:-2].split(":")
    HH = int(list_HHmm[0])
    mm = list_HHmm[1]
    period = time[-2:]

    if (period == "pm" and HH < 12) or (period == "am" and HH == 12):
        HH += 12
    return int(f"{HH}{mm}")


def check_available(timetable, new_event):
    """Check availability by comparing start, end time of the new event against all events in the same day"""

    # Timetable = empty means all slots are available
    if len(timetable) == 0:
        return True

    # Get list of events in the same day and return if it is empty
    same_day_events = []
    for event in timetable:
        if event['day'] == new_event['day']:
            same_day_events.append(event)
    
    if len(same_day_events) == 0:
        return True

    # Convert to numeric time format for old and new event and compare
    new_start = convert_time(new_event['start']) # new event start time
    new_end =  convert_time( new_event["end"]) # new event end time
    for old_event in same_day_events:
        old_start = convert_time(old_event["start"]) # old event start time
        old_end = convert_time(old_event["end"]) # old event end time
        
        # New event cannot start or end in existing event's timeslot
        if old_start <= new_start <= old_end or old_start <= new_end <= old_end:
            return False
    return True


def find_event_by_start(timetable, day, start) :
    """find an event by its starting time and day"""
    for event in timetable:
        if event["start"] == start and event["day"] == day:
            return event
        
    return


def update_event(timetable):
    """Find and Update an event's key values: title, day, start, end, location """
    #TODO: fix wording
    print("Select from below to search for event")
    print("Press 1 for day and start time")
    print("Press 2 for title")
    print("Press 3 for location")
    search_choice = input("Your choice is ")
    if search_choice == '1':
        # Find the event or return if no event found
        day = input("Day (e.g. monday, tue): ").lower()
        if not (check_day(day)):
            print("Invalid input due to incorrect format")
            return

        start = input("Time start (e.g. 10:30am, 1:00pm): ").replace(" ","").lower()
        if not check_time(start):
            print("Invalid input due to incorrect format")
            return

        event = find_event_by_start(timetable, day, start)
        if not event:
            print("No event found!")
            return
    elif search_choice =='2' or search_choice == '3':
        search_val = input('Search keyword: ')
        if search_choice == '2':
            events = find_events(timetable,'title',search_val)
        else:
            events = find_events(timetable,'location',search_val)
        print_events(events)
        event_choice = input("Select Event ID: ")
        try:
            event=events[int(event_choice)]
        except IndexError | TypeError:
            print("Invalid Choice")
            return
    else:
        print("Invalid Choice")
        return

    # Once the event is found, ask for updated inputs
    new_title = input("New Title (leave blank if no change): ")
    if not new_title:
        new_title = event["title"]

    new_day = input("New Day (leave blank if no change): ") 
    if not new_day:
        new_day = event["day"]

    new_start = (
        check_time(input("New Start Time (leave blank if no change): "))) 
    if not new_start:
        new_start = event["start"]
    
    new_end = check_time(input("New Time End (leave blank if no change): ")) 
    if not new_end:
        new_end = event["end"]
    
    new_loc = input("New Location (leave blank if no change): ") 
    if not new_loc:
        new_loc = event["location"]

    # Create new event
    new_event = {"title": new_title, "day": new_day, "start": new_start, "end": new_end, "location": new_loc}

    # Check if event is valid and if so then update the event, if not then keep old event
    timetable.remove(event)
    if check_available(timetable, new_event):
        timetable.append(new_event)
        print("Event updated succesfully")
    else:
        timetable.append(event)
        print("Event updated unsuccessfully")
    return

def print_events(events: list[dict[str, str]]) -> None:
    """Print events in a table format"""
    # Header
    print(
        "{:^4}|{:^26}|{:^5}|{:^9}|{:^9}|{:^22}".format(
            "ID","TITLE", "DAY", "START", "END", "LOCATION"
        )
    )
    print("—" *80)
    # Events
    for i in range(len(events)):
        print(
            "{id:^4}|{title:26}|{day:^5}|{start:^9}|{end:^9}|{location:22}".format(
                id=i,
                title=events[i]["title"][:26],
                day=events[i]["day"].capitalize(),
                start=events[i]["start"],
                end=events[i]["end"],
                location=events[i]["location"][:22],
            )
        )

    print("—" * 80)


def load_timetable(filename: str) -> list[dict[str, str]]:
    """Load timetable from a file and return empty list if fail"""
    tb = [] # list to take in events from file
    try:
        # open the file
        file = open(filename, 'r') 
        
        for line in file:
            # split the line into list
            tb_data = line.strip().split('|') # list that take in key values of an event
            
            # add values from file to event (dict)
            event = {
                'title': tb_data[0],
                'day': tb_data[1],
                'start': tb_data[2],
                'end': tb_data[3],
                'location': tb_data[4]
            }
            
            # add events to the list
            tb.append(event)

    except FileNotFoundError:
        print('File not accessible')
        return []
        
    # close the file
    file.close()
    return tb

def save_timetable(timetable: list[dict[str, str]], filename: str):
    """Save timetable into a txt file, separator is |, for each field"""
    try:
        file = open(filename,'w',encoding='utf-8')
        for event in timetable:
            line = "|".join(event.values()) + "\n" 
            file.write(line)
        return True
    except OSError:
        print('File not accessible')
        return False

def find_events(timetable, field, value):
    """Find events based on specific field and value"""
    events = [] 
    for event in timetable:
        if value.lower() in event[field].lower():
            events.append(event)
    return events

def sort_timetable(timetable, days):
    """Sort timetable according to day then start time in acensding order"""
    sorted_days = {}
    for i in range(len(days)):
        sorted_days[days[i]] = i
    
    timetable.sort(key=lambda e: (sorted_days[e["day"].capitalize()], convert_time(e["start"])))

if __name__ == "__main__":
    main()
