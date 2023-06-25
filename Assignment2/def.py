from pprint import pprint
from main import load_timetable, _convert_time, parse_time, shorten_info

data = load_timetable(r"Assignment2\timetable copy.txt")
line_template = "{:5}|{:10}|{:10}|{:10}|{:10}|{:10}|{:10}|{:9}"
days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
hours = ["", 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, ""]

h_col = []
# Construct Hour cols
for h in hours:
    h_col.extend([h, "", "-"])

tb = []
for h in hours:
    row = [h]
    row.extend([""] * len(days))
    tb.append(row)
    tb.append([""] * 8)
    tb.extend([["-" * 5] + ["-" * 10] * 8])
# Construct new events with flag
for event in data:
    rounded_start = _convert_time(event["start"]) // 100 * 100
    rounded_end = _convert_time(event["end"])
    col = days.index(event["day"].lower()) + 1

    if rounded_start < 900 or rounded_start > 1700:  # before work hours
        row = 0 if rounded_start < 900 else -3
        if not tb[row][col]:  # There is no event
            tb[row][col] = shorten_info("title", event["title"], 10)
            tb[row + 1][col] = shorten_info("time", f'{event["start"]}-{event["end"]}')
        elif not tb[row + 1][col]:  # There is 1 event already
            tb[row + 1][col] = shorten_info("title", event["title"], 10)
        else:  # More than 2 events 
            tb[row + 1][col] = ".etc"
    else:  # rounded_start <= 1600:  # Work hours
        row = h_col.index(rounded_start)
        time_span = rounded_end - rounded_start
        if time_span <= 100:  # Short event
            if not tb[row][col]:  # There is no event
                tb[row][col] = shorten_info("title", event["title"], 10)
                tb[row + 1][col] = shorten_info("location", event["location"], 10)
            elif not tb[row + 1][col]:  # There is 1 event already
                tb[row + 1][col] = shorten_info("title", event["title"], 10)
            else:  # More than 2 events 
                tb[row + 1][col] = ".etc"
        else:
            tb[row][col] = shorten_info("title", event["title"], 10)
            tb[row + 1][col] = shorten_info("location", event["location"], 10)
            tb[row + 2][col] = shorten_info("time", f'{event["start"]}-{event["end"]}')
            # Border delete tracker
            max_border = round((time_span) / 100) - 1
            i = 1
            while i < max_border:
                if (border := rounded_start + i * 100) > rounded_end:
                    i = max_border
                tb[h_col.index(border) + 2][col] = " " * 10
                i += 1
            # for i in range(1,max_border):
            #     if (border:= rounded_start + i*100) > rounded_end:
            #         break
            #     tb[h_col.index(border)+2][col] = ' '*10


print(line_template.format("", *days)[:80])
print(line_template.format(*["-" * 5] + ["-" * 10] * 8)[:80])
for row in tb[:-1]:
    print(line_template.format(*row)[:80])
