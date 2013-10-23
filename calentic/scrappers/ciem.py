# -*- coding: utf-8 -*-


from calendar_parser import CalendarParser


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

ciem_events = []
ics_url = "https://www.google.com/calendar/ical/" + \
    "ciemzaragoza%40gmail.com/public/basic.ics"


def getValue(node, value):
    """
        Try to get a value, casted as string
    """
    try:
        return str(node[value])
    except:
        return ""


def get_events():
    cal = CalendarParser(ics_url=ics_url)
    ics_events = cal.parse_calendar()

    for event in ics_events:
        ciem_events.append({
            'origin': 'CIEM',
            'title': getValue(event, "name"),
            'description': getValue(event, 'description'),
            'start_date': getValue(event, ' start_time'),
            'end_date': getValue(event, 'end_time'),
            'location': getValue(event, 'location'),
            'origin_url' : "http://ciemzaragoza.es",
        })

    return ciem_events

if __name__ == "__main__":
    get_events()
