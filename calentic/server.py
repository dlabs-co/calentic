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
import json
from flask.ext.pymongo import PyMongo

APP = Flask(__name__)
APP.config['MONGO_DBNAME'] = "calentic"
MONGO = PyMongo(APP)


@APP.route("/events/<start_date>/<end_date>/<place>")
def index(start_date=None, end_date=None, place=None):
    """
        Returns filtered events.
        <start_date>/<end_date>/place
        if you want it to not look at some param, just use None
        localhost/events/None/None/place
    """

    search_array = {}
    if start_date and start_date != "None":
        search_array['start_date'] = start_date
    if end_date and end_date != "None":
        search_array['end_date'] = end_date
    if place and place != "None":
        search_array['place'] = place

    return json.dumps([ ev for ev in MONGO.db.events.find(
        search_array
    )])

@APP.route("/")
def main():
    return render_template('index.html')

def server():
    """
        Main server, this will be executed on command, and with wsgi.
        This way we could still execute it in debug mode from normal console
        execution
    """
    APP.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=8081, debug=True)
