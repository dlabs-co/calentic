#!/usr/bin/env python
# encoding: utf-8
from mailer import Mailer, Message
from flask import render_template
from twitter import *

class Sender(object):
    """Communication engine"""

    def __init__(self, config):
        """
        Loads configuration, and logs in with twitter and mailer

        :config: configuration array

        """
        self._config = config

        self.twitter = Twitter(auth=OAuth(
            self._config['twitter']['oauth'][0],
            self._config['twitter']['oauth'][1],
            self._config['twitter']['oauth'][2],
            self._config['twitter']['oauth'][3]
        ))

        self.sender = Mailer('smtp.gmail.com', use_tls=True, port=587)
        self.sender.login(self._config['mail']['address'], self._config['mail']['pass'])

    def send_mail(self, html):
        """
            Send a mail via smtps
        """
        message = Message(
            From=self._config['mail']['address'], To=self._config['mail']['to'],
            Subject=self._config['mail']['subject']
        )
        message.Html = html
        return self.sender.send(message)

    def publish_twitter(event, event_url):
        """
            Simple twitter status update with the event url and title
        """
        return self.twitter.statuses.update(status='%s: %s' %(event, event_url))
