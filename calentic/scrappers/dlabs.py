# -*- coding: utf-8 -*-
from calendar_parser import CalendarParser
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
dlabs_events = []

ics_url = "http://www.dlabs.co/?wp-calendar-ical"

def get_events():
    cal = CalendarParser(ics_url=ics_url)


    ics_events = cal.parse_calendar()

    for event in ics_events:
        try:
            eventdlabs = {
                'origin': 'Dlabs',
                'title': event['name'],
                'description': event['description'],
                'start_date': str(event['start_time']),
                'end_date': str(event['end_time']),
                'location': "Dlabs - Calle camino de la mosquetera 41",
                'origin_url' : "http://dlabs.co",
            }

            dlabs_events.append(eventdlabs)

        except KeyError:
            eventdlabs = {
                'origin': 'dlabs',
                'title': event['name'],
                'description': event['description'],
                'start_date': str(event['start_time']),
                'end_date': str(event['end_time']),
                'origin_url' : "http://dlabs.co",
            }

            dlabs_events.append(eventdlabs)

    return dlabs_events

if __name__ == "__main__":
    print json.dumps(get_events())
