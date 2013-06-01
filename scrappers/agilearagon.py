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
agile_events = []

ics_url = "https://www.google.com/calendar/ical/agileenaragon%40gmail.com/public/basic.ics"

def get_events():
    cal = CalendarParser(ics_url=ics_url)
    
    
    ics_events = cal.parse_calendar()
    
    for event in ics_events:
        try:
            eventAgile = {
                'origin': 'Agile Aragón',
                'title': event['name'],
                'description': event['description'],
                'start_date': str(event['start_time']),
                'end_date': str(event['end_time']),
                'location': event['location'],
            }
        
            agile_events.append(eventAgile)
        
        except KeyError:
            eventAgile = {
                'origin': 'Agile Aragón',
                'title': event['name'],
                'description': event['description'],
                'start_date': str(event['start_time']),
                'end_date': str(event['end_time']),
            }
        
            agile_events.append(eventAgile)
    
    return json.dumps(agile_events)
        
get_events()