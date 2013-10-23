import urllib2
from xml.dom import minidom

BASE_URL = "http://www.observatorioaragones.org/forostic/"
FEED_URL = "http://www.google.com/calendar/feeds/forosticaragon%40gmail.com" +\
    "/private-802f258df2d9b737b847178a508654dc/full"


def get_value(name, node):
    """
        Returns the text value of a node
    """
    return node.getElementsByTagName(name)[0].firstChild.nodeValue


def get_events():
    """
        Get the events
    """
    response = urllib2.urlopen(FEED_URL)
    atom = response.read()
    dom = minidom.parseString(atom)
    results = []

    for node in dom.getElementsByTagName('entry'):
        print node.getElements
        dates = node.getElementsByTagName('gd:when')[0].attributes
        results.append({
            'origin': 'ForosTic',
            'url' : False,
            'title': get_value("title", node),
            'description': get_value("content", node),
            'start_date': dates['startTime'].value,
            'end_date': dates['endTime'].value,
            'location': node.getElementsByTagName('gd:where')[0].nodeValue,
            'origin_url' : BASE_URL,
        })
    return results

if __name__ == "__main__":
    get_events()
