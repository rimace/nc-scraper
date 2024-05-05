import nc
import csv

event_table_url_list = [
    "https://db.nipponconnection.com/de/2024/event/timetable?page=1",
    "https://db.nipponconnection.com/de/2024/event/timetable?page=2",
    "https://db.nipponconnection.com/de/2024/event/timetable?page=3",
    "https://db.nipponconnection.com/de/2024/event/timetable?page=4",
    "https://db.nipponconnection.com/de/2024/event/timetable?page=5",
    "https://db.nipponconnection.com/de/2024/event/timetable?page=6",
    "https://db.nipponconnection.com/de/2024/event/timetable?page=7",
]

event_pages = []

for event_table_url in event_table_url_list:
   event_pages += nc.get_pages(event_table_url)

for event in event_pages:
    print("Parsing: " + event.url)
    event.parse()

with open("test.csv", 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for event in event_pages:
         wr.writerow(event)

