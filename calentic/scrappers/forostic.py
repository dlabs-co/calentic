import urllib2
from xml.dom import minidom

BASE_URL = "http://www.observatorioaragones.org/forostic/"
FEED_URL = "http://www.google.com/calendar/feeds/forosticaragon%40gmail.com" +\
"/private-802f258df2d9b737b847178a508654dc/full"

def get_events():
    response = urllib2.urlopen(FEED_URL)
    atom = response.read()

    try:
        dom = minidom.parseString(atom)
        #print arbol_dom.toxml()
    except Exception, err:
        print err
        print "Error: can't read file"

    # Ejemplo para sacar titulos
    for node in dom.getElementsByTagName('title'):
        print node.firstChild.nodeValue

    # Y muy importante: fechas
    for node in dom.getElementsByTagName('gd:when'):
        print "Inicio: "+node.attributes['startTime'].value+" - Fin: "+\
              node.attributes['endTime'].value

if __name__ == "__main__":
    get_events()
