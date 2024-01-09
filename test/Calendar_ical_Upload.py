import datetime
import re

# Define a function to parse date and time from the text
def parse_date_time(date_str, time_str):
    date = datetime.datetime.strptime(date_str, '%A, %B %d')
    time = datetime.datetime.strptime(time_str, '%I:%M%p').time()
    return datetime.datetime.combine(date.date(), time)

# Read the text file
with open('target_schedule.txt', 'r') as file:
    lines = file.readlines()

# Parse the events from the text file
events = []
current_event = None
for line in lines:
    line = line.strip()
    if re.match(r'^[A-Z][a-z]+, [A-Z][a-z]+ \d{1,2}$', line):  # Match day format
        day = line
        print(f"Day: {day}")
    elif re.match(r'^\d{1,2}:\d{2}(AM|PM)$', line):  # Match time format
        time = line
        print(f"Time: {time}")
    elif line:  # Non-empty line, consider it as event content
        content = line
        if day and time:
            start_datetime = parse_date_time(day, time)
            end_datetime = start_datetime + datetime.timedelta(hours=1)  # Assuming 1-hour event duration
            event = {
                'summary': content,
                'start': start_datetime,
                'end': end_datetime,
            }
            events.append(event)
            print(f"Event parsed: {event}")

# Generate the iCal file
ical = "BEGIN:VCALENDAR\nVERSION:2.0\n"
for event in events:
    ical += "BEGIN:VEVENT\n"
    ical += f"SUMMARY:{event['summary']}\n"
    ical += f"DTSTART:{event['start'].strftime('%Y%m%dT%H%M%S')}\n"
    ical += f"DTEND:{event['end'].strftime('%Y%m%dT%H%M%S')}\n"
    ical += "END:VEVENT\n"
ical += "END:VCALENDAR"

# Save the iCal file
with open('calendar.ics', 'w') as file:
    file.write(ical)

print("iCal file generated successfully.")
