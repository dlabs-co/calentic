# -*- coding: utf-8 -*-
from  calentic.scrappers.calendar_parser import CalendarParser
import json
import sys


"""
ORIGIN:
IMAGE:
TITLE:
DESCRIPTION:
START_DATE:
END_DATE:
LOCATION:
GEOLOCATION:
REGISTRATION_URL:
"""
reload(sys)
sys.setdefaultencoding("utf-8")
ciem_events = []

ics_url = "https://www.google.com/calendar/ical/ciemzaragoza%40gmail.com/public/basic.ics"

def get_events():
    cal = CalendarParser(ics_url=ics_url)


    ics_events = cal.parse_calendar()

    for event in ics_events:
        try:
            eventCiem = {
                'origin': 'CIEM',
                'title': event['name'],
                'description': event['description'],
                'start_date': str(event['start_time']),
                'end_date': str(event['end_time']),
                'location': event['location'],
            }

            ciem_events.append(eventCiem)

        except KeyError:
            eventCiem = {
                'origin': 'CIEM',
                'title': event['name'],
                'description': event['description'],
                'start_date': str(event['start_time']),
                'end_date': str(event['end_time']),
            }

            ciem_events.append(eventCiem)

    return ciem_events

if __name__ == "__main__":
    get_events()

