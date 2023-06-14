from main import load_timetable, _convert_time


timetable = load_timetable(r"Assignment2\timetable.txt")
# Print Header
template = "{:7}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}"
print(template.format("", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"))
timetable_list = []
for i in range(7, 17):
    # timetable_list.append(template.format(f"{i:02d}am", *[""] * 7))
    for event in timetable:
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

    print(template.format(f"{i:02d}am", *line))
    print(template.format(*[""] * 8))


# Define the timetable data
# timetable = [
#     ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
#     ["9:00 AM", "Math", "English", "Biology", "Physics", "Chemistry"],
#     ["10:00 AM", "History", "Geography", "Art", "Music", "Physical Education"],
# ]


# # Function to calculate the maximum width of each column
# def get_max_widths(table):
#     max_widths = [0] * len(table[0])
#     for row in table:
#         for i, item in enumerate(row):
#             max_widths[i] = max(max_widths[i], len(item))
#     return max_widths


# # Function to print a row with borders
# def print_row(row, max_widths):
#     for i, item in enumerate(row):
#         print("|", end="")
#         print(item.ljust(max_widths[i]), end="")
#     print("|")


# # Calculate the maximum width of each column
# max_widths = get_max_widths(timetable)

# # Print the timetable with borders
# for row in timetable:
#     print("-" * (sum(max_widths) + 5 * len(row) - 1))
#     print_row(row, max_widths)
# print("-" * (sum(max_widths) + 5 * len(row) - 1))
