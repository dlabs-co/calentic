#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize
from icalendar import Calendar, Event
import json

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

DATE_FORMAT = '%Y-%m-%d %H:%M'
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


def set_content(events_list):
    """
    Encode json from events.
    """
    data = []

    for event in events_list:
        title = event.get("SUMMARY")
        description = event.get("DESCRIPTION")
        start_date = event.get("DTSTART").dt.strftime(DATE_FORMAT)
        end_date = event.get("DTEND").dt.strftime(DATE_FORMAT)
        location = event.get("LOCATION")
        url = event.get('REGISTRATION_URL')

        data.append({
            'origin' : u"betabeers",
            'origin_url' : u"http://www.betabeers.com",
            'title': title,
            'url' : str(description),
            'description': "",
            'start_date': start_date,
            'end_date': end_date,
            'location': location
        })
    return data


def set_json_content(data):
    return json.dumps(
        data, ensure_ascii=False,
        separators=(",", ":"), sort_keys=False
    )


def get_events():
    ics = get_ics_calendar(URL)
    events = set_content(get_events_from_calendar(ics))
    return events

if __name__ == '__main__':
    print get_events()
