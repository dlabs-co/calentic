# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.ita.es/ita/"
ita_events = [] #The empty list where the EventITA instances will be stored and returned at the end of get_events function

class EventITA:
    def __init__(self, title, description, date, event_url):
        self.origin = "ITA"
        self.title = title
        self.description = description
        self.date = date
        self.event_url = event_url

def get_events(section_url = "http://www.ita.es/ita/?eventos"):
    """
    When get_events() is executed, a group of EventITA objects are created and stored in ita_events list
    """
    html = urlopen(section_url).read()
    soup = BeautifulSoup(html, "lxml")
    ita_items = soup.find("section", "ita-items")
    
    event_links = [BASE_URL + a["href"] for a in ita_items.findAll("a")]
    
    event_titles = []
    temp = ita_items.find_all("h3")
    for item in temp:
       for subitem in str(item).split("</small>"):
           if "<small>" in subitem:
               pass
           else:
               if "</h3>" in subitem:
                   if "<h3>" in subitem:
                       event_titles.append(subitem[4:-5])
                   else:
                       event_titles.append(subitem[1:-5])
    
    event_dates = []
    months = {'Ene':'01', 'Feb':'02', 'Mar':'03', 'Abr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Ago':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dic':'12'}
    for h4 in ita_items.findAll("h4"):
        temp = str(h4)[4:-5].split()
        copy_temp = temp
        temp[1] = months[copy_temp[1]]
        event_dates.append("/".join(temp))
    
    event_descriptions = dict()
    temp = ita_items.findAll("a")
    for item in temp:
        if "<p>" in str(item):
            temp2 = item.findAll("p")
            if "<small>" in str(temp2):
                for item2 in temp2:
                    for subitem2 in str(item2).split("<small>"):
                        if "</small>" in str(subitem2):
                            pass
                        
                        else:
                            description = subitem2[3:]
                            event_descriptions[BASE_URL + item["href"]] = str(description)

            
            else:
                event_descriptions[BASE_URL + item["href"]] = None
        
        else:
            event_descriptions[BASE_URL + item["href"]] = None
    
    for n in range(len(event_titles)):
        eventObject = EventITA(event_titles[n], event_descriptions[event_links[n]], event_dates[n], event_links[n])
        
        if eventObject in ita_events:
            pass
        
        else:
            ita_events.append(eventObject)
    
    return ita_events
