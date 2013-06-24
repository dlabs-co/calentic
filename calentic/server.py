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

from flask import Flask, render_template
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId
from calentic.scrappers import *

import calentic.scrappers
import json as _json
import os


APP = Flask(__name__)
if "MONGOHQ_URL" in os.environ.keys():
    APP.config['MONGO_URI'] = os.environ["MONGOHQ_URL"]
else:
    APP.config['MONGO_DB'] = "calentic"

MONGO = PyMongo(APP)


class JSONEncoder(_json.JSONEncoder):
    """
       Replacing
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return ""
        return _json.JSONEncoder.default(self, o)


@APP.route("/events/<path:route>")
def index(route):
    """
        Returns filtered events.
        /events/elem=foo/elem=bar/elem=baz
    """

    allowed_params = ["start_date", "end_date", "place", "origin"]
    search = {}
    for param_ in route.split("/"):
        param = param_.split("=")
        if param[0] in allowed_params:
            search[param[0]] = param[1]

    return JSONEncoder().encode([ev for ev in MONGO.db.events.find(
        search
    )])


@APP.route('/repopulate')
def cron():
    db = MONGO.db.events
    for scrapper in calentic.scrappers.__all__:
        mod = getattr(calentic.scrappers, scrapper)
        events = getattr(mod, "get_events")()
        errors = ""
        events_ = ""
        if events:
            for event in events:
                try:
                    if not db.find_one({'title': event['title']}):
                        db.insert(event)
                        events_ += "<br/> Event %s inserted" % (
                            event['title']
                        )
                    else:
                        errors += "<br/>Event %s already inserted." % (
                            event['title']
                        )
                except:
                    errors += "<br/>For some reason, event %s - %s failed" % (
                        scrapper, event
                    )
        else:
            errors += "Could not get any event from: "
            errors += "%s" % mod
        return render_template(
            'repopulate.html',
            errors=errors,
            events_=events_
        )


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
    APP.run(host='0.0.0.0', port=8081, debug=True)
