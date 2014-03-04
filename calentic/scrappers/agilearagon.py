#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from calentic.utils.calendar_parser import CalendarParser, parse_ical

ics_url = "https://www.google.com/calendar/ical/agileenaragon%40gmail.com/public/basic.ics"
defaults = {
    'origin' : u"Agile Aragón",
    'origin_url' : u'http://agile-aragon.org'
}

def get_events():
    return parse_ical(ics_url, defaults)

