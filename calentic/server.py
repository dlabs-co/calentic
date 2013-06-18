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
import json as _json
import os
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId
import calentic.scrappery


APP = Flask(__name__)
APP.config['MONGO_URI'] = os.environ["MONGOHQ_URL"]
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


@APP.route('/cron')
def cron():
    calentic.scrappery.main()

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
