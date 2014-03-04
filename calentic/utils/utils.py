#!/usr/bin/env python
# encoding: utf-8

'''
    File: utils.py
    Author: David Francos
    Description: Stuff that I'm not sure where to put
'''

import json as _json
import time
import datetime
from time import strptime, mktime
from dateutil import parser
from flask import render_template
from bson.objectid import ObjectId

class Event(object):
    """Event"""

    def __init__(self, raw_event):
        """
            :raw_event: raw event data, unprocessed
        """
        self._raw_event = raw_event

    def get_formatted_html(self):
        external_url = self._raw_event.get('externalurl', False)
        event = self.format_data()
        if external_url:
            event['url'] = {
                'url' : externalurl,
                'name' : externalurl
            }
        else:
            old_event_url = event['url']
            event["url"] = {
                'url' : old_event_url,
                'name' : u"Más Información"
            }

        return render_template("single_event.html", event=event)

    def get(self, element, default="", append="", link=False):
        """
            Return default for object_[element] with the extra append stuff
        """
        result = self._raw_event.get(element, "")
        if result != "":
            return result + append
        elif link:
            return "<a href=" + link + ">" + default + "</a>"
        return default

    def format_data(self):
        """
            Return the event with default values.
        """

        return {
            "title" : self.get('title', ""),
            "origin_url": self.get('origin_url', ""),
            "origin_name": self.get('origin', ""),
            "url"   : '/event/' + str(self._raw_event['_id']),
            "externalurl" : self.get("url", ""),
            'location' : self.get("location", ""),
            'description': self.get("description", "Leer más", "...", self.get("url", False)),
            "start" : time.mktime(parser.parse(self.get('start_date')).timetuple()) * 1000,
            "end"   : time.mktime(parser.parse(self.get('end_date')).timetuple()) * 1000,
            "class" : 'event-warning'
        }

    def __repr__(self):
        return _json.dumps(self.format_data())

class JSONEncoder(_json.JSONEncoder):
    """
       Replacing jsonencoder so it can handle objectids
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return ""
        return _json.JSONEncoder.default(self, o)


def dateformat(date):
    """
        Format date in a more web appropiate way
    """
    return datetime.datetime.fromtimestamp(int(int(date) / 1000)).strftime('%Y-%m-%d %H:%M:%S')


