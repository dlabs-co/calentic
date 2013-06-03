![CalenTIC](http://i.imgur.com/K66uwfm.png)

Unified Zaragoza ICT Events (TIC in Spanish) calendar
=======================================================

About
------

Tired of having to check all the different sources for technological events
in zaragoza we decided to do a calendar that scrapes every one of them and
presents the data in a nice form and a API

Dependences
--------------

    pip install -r deps

Running
---------------

You have the calentic executable for standalone running, the examples/crontab
file contains a valid crontab wich will launch the scrappers and populate the
mongodb database every day and the wsgi and lighttpd config in examples/
Have fun! 
