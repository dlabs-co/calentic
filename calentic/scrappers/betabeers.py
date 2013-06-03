#!/usr/bin/env python
# -*- coding: utf-8 -*-


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


import mechanize
from icalendar import Calendar, Event
import json
from collections import OrderedDict


DATE_FORMAT = "%a %d-%m-%Y %H:%M"
URL = "http://betabeers.com/event/ical/?province_id=Z"


def get_ics_calendar(url=URL):
    """
    Get icalendar from website.
    """
    response = mechanize.urlopen(url)
    response = response.read()
    return response

def get_events_from_calendar(ics):
    """
    Return a list with all events.
    """
    calendar = Calendar.from_ical(ics)
    events = [event for event in calendar.walk() if isinstance(event, Event)]
    return events

def set_json_content(events_list):
    """
    Encode json from events.
    """
    json_data = []

    for event in events_list:
        title = event.get("SUMMARY")
        description = event.get("DESCRIPTION")
        start_date = event.get("DTSTART").dt.strftime(DATE_FORMAT)
        end_date = event.get("DTEND").dt.strftime(DATE_FORMAT)
        location = event.get("LOCATION")

        data = OrderedDict([('title', title),
                            ('description', description),
                            ('start_date', start_date),
                            ('end_date', end_date),
                            ('location', location)])
        json_data.append(data)

    final_json = json.dumps(json_data, ensure_ascii=False,
                            separators=(",", ":"), sort_keys=False)
    return final_json


def get_events():
    ics = get_ics_calendar(URL)
    events = get_events_from_calendar(ics)
    return set_json_content(events)

if __name__ == '__main__':
    get_events()
