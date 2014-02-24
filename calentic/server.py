#!/usr/bin/env python
# - coding:utf-8 - #
"""
    TIC Calendar

    Copyright (C) 2013 Zaragoza Python User Group

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
    USA.

"""

from flask import Flask, request, render_template
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId
from calentic.scrappers import *
from flask import Flask, render_template, flash, session, redirect, url_for
from calentic.utils.twitter_calentic import *
from calentic.utils.mail_calentic import *
import calentic.scrappers
import json as _json
import os
import time
import datetime
from time import strptime, mktime
from dateutil import parser

def get(object_, element, default, append="", link=False):
    if element in object_ and object_[element] != "":
        return object_[element] + append
    elif link:
        return "<a href=" + link + ">" + default + "</a>"
    else:
        return default

def format_event(ev):
    """
        Return the event with default values.
    """

    a = {
        "title" : get(ev, 'title', ""),
        "origin_url": get(ev, 'origin_url', ""),
        "origin_name": get(ev, 'origin', ""),
        "url"   : '/event/' + str(ev['_id']),
        "externalurl" : get(ev, "url", ""),
        'location' : get(ev, "location", ""),
        'description': get(ev, "description", "Leer más", "...", get(ev, "url", False)),
        "start" : time.mktime(parser.parse(ev['start_date']).timetuple()) * 1000,
        "end"   : time.mktime(parser.parse(ev['end_date']).timetuple()) * 1000,
        "class" : 'event-warning'
    }
    return a

def dateformat(date):
    """
        Format date.
    """
    return datetime.datetime.fromtimestamp(int(int(date) / 1000)).strftime('%Y-%m-%d %H:%M:%S')

class JSONEncoder(_json.JSONEncoder):
    """
       Replacing
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return ""
        return _json.JSONEncoder.default(self, o)



APP = Flask(__name__)
if "MONGOHQ_URL" in os.environ.keys():
    APP.config['MONGO_URI'] = os.environ["MONGOHQ_URL"]
else:
    APP.config['MONGO_DB'] = "calentic"

MONGO = PyMongo(APP)

RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
SECRET_KEY="foo"

def do_create_event(event):
    MONGO.db.events.insert(event)
    send_mail(event['title'], event['url'], event['description'])
    publish_twitter(event['title'], event['url'])

@APP.route('/event/<oid>', methods=["POST", "GET"])
def event(oid):
    events = [format_event(ev) for ev in MONGO.db.events.find({ '_id' : ObjectId(oid) }) ]
    url = ""
    if events[0]['externalurl']:
        url = "<a href='" + events[0]['externalurl'] + "'>" + events[0]['externalurl'] + "</a>"
    return "<div><h1>" + events[0]['title'] +"</h1><address>"+events[0]["location"]+"</address><p>" + events[0]['description'] + "</p>" + url

@APP.route("/create_event/", methods=['POST', 'GET'])
def create_event():
    if request.method == "POST":
        do_create_event(request.form.copy().to_dict(flat=True))
        return redirect("/")
    else:
        return render_template(
            'add_event.html'
        )

@APP.route("/events/<path:route>", methods=['POST', 'GET'])
def index(route):
    """
        Returns filtered events.
        /events/elem=foo/elem=bar/elem=baz
    """

    allowed_params = ["start_date", "end_date", "place", "origin"]
    search = {}
    for param_ in route.split("/"):
        param = param_.split("=")
        if "from" in request.form.values():
            search["start_date"] = {
                '$gt' : dateformat(request.form['from'])
            }
            search["end_date"] = {
                '$lt'  : dateformat(request.form['to'])
            }
        elif param[0] in allowed_params:
            if "date" in param[0]:
                if "end" in param[0]:
                    status = '$lt'
                else:
                    status = '$gt'

                search[param[0]] = {
                    status : dateformat(param[1])
                }
            else:
                search[param[0]] = param[1]
    events = [format_event(ev) for ev in MONGO.db.events.find(search)]
    if len(events) > 0:
        return JSONEncoder().encode(dict({
            'events' : events,
            'success': True
        }))
    else:
        return ""

@APP.route('/repopulate')
def cron():
    result = []
    for scrapper in calentic.scrappers.__all__:
        try:
            events = getattr(
                getattr(calentic.scrappers, scrapper), "get_events"
            )()
            for event in events:
                try:
                    if not MONGO.db.events.find_one({'title': event['title']}):
                        do_create_event(event)
                    result.append("Event %s added" % event['title'])
                except Exception, error:
                    result.append("Failed " + event['title' ] + ": " + error)

        except Exception, err:
            print "Error happened while trying to retrieve %s events:%s" % (
                scrapper, err
            )
            continue
    return _json.dumps(result)

@APP.route("/")
def main():
    """
       Render template
    """
    return render_template(
        'index.html',
        events=JSONEncoder().encode([ev for ev in MONGO.db.events.find()])
    )


def server():
    """
        Main server, this will be executed on command, and with wsgi.
        This way we could still execute it in debug mode from normal console
        execution
     """
    APP.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    APP.config['SECRET_KEY'] = "FOO"
    APP.config['secret_key'] = "FOO"
    APP.run(host='0.0.0.0', port=8081, debug=True)
