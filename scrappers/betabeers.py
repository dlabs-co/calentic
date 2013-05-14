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


URL = "http://betabeers.com/event/ical/"
# URL = "http://betabeers.com/event/ical/?province_id=Z"


def get_ics_calendar(url=URL):
    """
    Get icalendar from website.
    """
    response = mechanize.urlopen(url)
    response = response.read()
    return response

def get_events_from_calendar(ics):
    """
    Get events from icalendar.
    """
    calendar = Calendar.from_ical(ics)
    events = [event for event in calendar.walk() if isinstance(event, Event)]

    for event in events:
        title = event.get("SUMMARY")
        description = event.get("DESCRIPTION")
        start_date = event.get("DTSTART").dt
        end_date = event.get("DTEND").dt
        location = event.get("LOCATION")
        print "%s\n%s\n%s\n%s\n%s" % (title, description, start_date, end_date, 
                                      location)
 


def main():
    ics = get_ics_calendar(URL)
    get_events_from_calendar(ics)





if __name__ == '__main__':
    main()
