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
from calentic.scrappers import *
import calentic.scrappers
import pymongo


def main():
    """
        Connects to a mongo database, executes
        all the scrappers and put the events in
        place in case they're not there already
    """

    client = pymongo.MongoClient("localhost", 27017)
    db = client.calentic
    for scrapper in calentic.scrappers.__all__:
        mod = getattr(calentic.scrappers, scrapper)
        events = getattr(mod, "get_events")()
        # TODO This is somehow how it should be, untested
        # Amazing, btw.
        for event in events:
            if not db.events.find({'title': event['title']}):
                # Dont save events we already have.
                db.events.save(event)

if __name__ == "__main__":
    main()
