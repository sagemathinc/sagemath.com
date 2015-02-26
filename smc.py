#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import datetime
import logging
import webapp2
import jinja2
import urllib
import urllib2
import json

captcha_secret = "6LdNmQITAAAAAHPYZZpLFhO2EuG3dgyhOlCOmkmo"

YEAR = str(datetime.date.today().year)
# DEBUG==False -> we are deployed on GAE
DEBUG = not os.environ['SERVER_SOFTWARE'].startswith('Google App Engine')
GLOBAL_VALS = {
    "year": YEAR,
    "email": "info@sagemath.com",
    "smc": "SageMathCloud",
    "company": "SageMath, Inc.",
    "slogan": "Collaborative Computational Mathematics Online."
}

TMPL_EMAIL = u"""\
Name:       {name}
Email:      {email}
Telephone:  {tel}
Subject:    {subject}
Timestamp:  {timestamp}
IP:         {ip}

{message}
"""

j2env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('Hello, World!')

        vals = {}
        vals.update(GLOBAL_VALS)
        template = j2env.get_template('index.html')
        self.response.write(template.render(vals))


class ContactForm(webapp2.RequestHandler):
    def post(self):
        timestamp = str(datetime.datetime.utcnow())[:16]
        ip = self.request.remote_addr

        # check captcha
        captcha_response = self.request.get("g-recaptcha-response")
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        request_data = urllib.urlencode({
            'secret': captcha_secret,
            'remoteip': ip,
            'response': captcha_response
        })
        captcha_req = urllib2.Request(url=captcha_url, data=request_data)
        try:
            captcha_resp = urllib2.urlopen(captcha_req, timeout=10)
            logging.debug("captcha response: %s" % captcha_resp)

            if not json.loads(captcha_resp.read())["success"]:
                self.error(500)
        except:
            # error with captcha service, continue as nothing would have happened
            pass

        # logging.info("data: %s" % self.request)

        fields = {}
        for k in self.request.arguments():
            fields[k] = self.request.get(k)
            #logging.info("fields: %s -> %s" % (k, self.request.get(k)))

        from google.appengine.api import mail
        msg = mail.EmailMessage()
        msg.sender="{name} <{email}>".format(**fields)
        msg.subject="[SMC.com] %s" % fields.get("subject")
        #msg.to = "SageMath Inc. <contact+website@sagemath.com>"
        msg.to = "SageMath Inc. <hsy+website@sagemath.com>"
        msg.body = TMPL_EMAIL.format(timestamp=timestamp, ip = ip, **fields)
        msg.send()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write("{ 'success': 'true' }")


class Stats(webapp2.RequestHandler):
    def get(self):
        import urllib2
        try:
            stats = urllib2.urlopen('https://cloud.sagemath.com/stats').read()
            self.response.write(stats)
        except:
            self .error(500)

routing = [
    ('/',           MainPage),
    ('/contact',    ContactForm),
    ('/stats',      Stats)
]
app = webapp2.WSGIApplication(routing, debug=DEBUG)
