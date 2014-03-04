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
from calentic.utils.private import sender_config
from calentic.utils.comunication import Sender
from calentic.utils.utils import Event, JSONEncoder, dateformat
import calentic.scrappers
import os
import sys

APP = Flask(__name__)
if "MONGOHQ_URL" in os.environ.keys():
    APP.config['MONGO_URI'] = os.environ["MONGOHQ_URL"]
else:
    APP.config['MONGO_DB'] = "calentic"

MONGO = PyMongo(APP)
sender=Sender(sender_config)

def do_create_events(events):
    """
        Create events.
    """
    for event in events:
        MONGO.db.events.insert(event)
        publish_twitter(event['title'], event['url'])

    sender.send_mail(render_template('mail_base.html', events = events))

    return True

@APP.route('/event/<oid>', methods=["POST", "GET"])
def event(oid):
    return [Event(ev) for ev in MONGO.db.events.find({ '_id' :
        ObjectId(oid) }) ][0].get_formatted_html()

@APP.route("/create_event/", methods=['POST', 'GET'])
def create_event():
    if request.method == "POST":
        do_create_events([request.form.copy().to_dict(flat=True)])
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
        if param_ != "all":
            name, value = param_.split("=")

        if "from" in request.form.values():
            search["start_date"] = {'$gt' : dateformat(request.form['from'])}
            search["end_date"] = {'$lt'  : dateformat(request.form['to'])}
        elif param_ != "all" and name in allowed_params:
            if "date" in name:
                status = '$gt'
                if "end" in name:
                    status = '$lt'
                search_query = {status : dateformat(value)}
            else:
                search_query = value
            search[name] = value

    events = [Event(ev).format_data() for ev in MONGO.db.events.find(search)]

    if len(events) > 0:
        return JSONEncoder().encode(dict({
            'events' : events,
            'success': True
        }))

    return ""

@APP.route('/repopulate')
def cron():
    errors = []
    added_events = []
    for scrapper in calentic.scrappers.__all__:
        try:
            events = getattr(
                getattr(calentic.scrappers, scrapper), "get_events"
            )()
        except Exception, err:
            continue

        for event in events:
            try:
                if not MONGO.db.events.find_one({'title': event['title']}):
                    added_events.append(event)
            except Exception, error:
                errors.append({
                    "status": "failed",
                    "title": event['title' ],
                    "Error": error
                })

        do_create_events(added_events)

    if errors != []:
        return JSONEncoder().encode(errors)
    else:
        return JSONEncoder().encode(added_events)

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
        execution)
     """
    APP.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=8081, debug=True)
