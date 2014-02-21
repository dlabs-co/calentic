#!/usr/bin/env python
# -*- coding: utf-8 -*-
from calentic.utils.calendar_parser import CalendarParser
import json
import sys
# Distributed under GNU/GPL 2 license

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/

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
                'location': "C/Camino de la mosquetera 41",
                'url' : str(event['url']),
                'origin_url' : "http://www.dlabs.co",
            }

            dlabs_events.append(eventdlabs)

        except KeyError:
            eventdlabs = {
                'origin': 'dlabs',
                'location': "C/Camino de la mosquetera 41",
                'title': event['name'],
                'description': event['description'],
                'url' : str(event['url']),
                'start_date': str(event['start_time']),
                'end_date': str(event['end_time']),
                'origin_url' : "http://www.dlabs.co",
            }

            dlabs_events.append(eventdlabs)

    return dlabs_events

if __name__ == "__main__":
    print json.dumps(get_events())
