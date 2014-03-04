#!/usr/bin/env python
# -*- coding: utf-8 -*-
from calentic.utils.calendar_parser import CalendarParser, parse_ical

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

ics_url = "http://www.dlabs.co/?wp-calendar-ical"
defaults = {
    'origin' : u"Dlabs Hackerspace",
    'origin_url' : u'http://dlabs.co'
}

def get_events():
    return parse_ical(ics_url, defaults)

