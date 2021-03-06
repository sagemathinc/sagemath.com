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

# DEBUG==False -> we are deployed on GAE
DEBUG = not os.environ['SERVER_SOFTWARE'].startswith('Google App Engine')

captcha_secret = "6LdNmQITAAAAAHPYZZpLFhO2EuG3dgyhOlCOmkmo"

YEAR = str(datetime.date.today().year)

ANALYTICS = r"""
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-34321400-2', 'auto');
  ga('send', 'pageview');

</script>
"""

GLOBAL_VALS = {
    "DEBUG" : DEBUG,
    "analytics": ANALYTICS,
    "year": YEAR,
    "email": "info@sagemath.com",
    "smc": "SageMathCloud",
    "smcurl": "https://cloud.sagemath.com/",
    "company": "SageMath, Inc.",
    "slogan": "Collaborative Computational Mathematics"
}

# double {{ }} for { } because {fields} are replaced via string.format()
TMPL_EMAIL = u"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<style>
body {{ font-family:‘Lucida Console’, Monaco, monospace; }}
table {{border-collapse: collapse; }}
table td {{ padding: 10px; }}
</style>
</head>
<body style="font-family:‘Lucida Console’, Monaco, monospace;">
<table border="1">
<tr><td>Name:</td>      <td>{name}</td></tr>
<tr><td>Email:</td>     <td>{email}</td></tr>
<tr><td>Telephone:</td> <td>{tel}</td></tr>
<tr><td>Subject:</td>   <td>{subject}</td></tr>
<tr><td>Timestamp:</td> <td>{timestamp}</td></tr>
<tr><td>IP:</td>        <td>{ip}</td></tr>
<tr><td colspan="2">
{message}
</td></tr>
</table>
</body>
</html>
"""

j2env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        # demo example
        # self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('Hello, World!')

        # what has been before to show the page
        #vals = {}
        #vals.update(GLOBAL_VALS)
        #template = j2env.get_template('index.html')
        #self.response.write(template.render(vals))

        # redirect to SMC instead
        self.redirect('https://cloud.sagemath.com/')


class ContactForm(webapp2.RequestHandler):
    def post(self):
        timestamp = str(datetime.datetime.utcnow())[:16]
        ip = self.request.remote_addr

        # check captcha
        if False:
            captcha_response = self.request.get("g-recaptcha-response")
            captcha_url = "https://www.google.com/recaptcha/api/siteverify"
            request_data = urllib.urlencode({
                'secret': captcha_secret,
                'remoteip': ip,
                'response': captcha_response
            })
            captcha_req = urllib2.Request(url=captcha_url, data=request_data)
            try:
                captcha_resp = urllib2.urlopen(captcha_req, timeout=10).read()
                logging.debug("captcha response: %s" % captcha_resp)

                if not json.loads(captcha_resp)["success"]:
                    self.error(500)
            except:
                # error with captcha service, continue as nothing would have happened
                pass
        # END captcha check

        fields = {}
        for k in self.request.arguments():
            fields[k] = self.request.get(k)
            #logging.info("fields: %s -> %s" % (k, self.request.get(k)))

        # we have all data, now sending the mail to the smc headquarter
        from google.appengine.api import mail
        msg = mail.EmailMessage()
        msg.sender="SMC Website <website@sage-math-inc.appspotmail.com>"
        msg.subject="[SMC.com] %s" % fields.get("subject")
        msg.to = "SageMath Inc. <contact+website@sagemath.com>"
        #msg.to = "hsy@sagemath.com"
        msg.html = TMPL_EMAIL.format(timestamp=timestamp, ip = ip, **fields)
        msg.send()

        self.response.headers['Content-Type'] = 'application/json'
        #self.response.write(json.dumps({ 'success': True }))
        self.response.write("{ 'success': 'true' }")


class Stats(webapp2.RequestHandler):
    def get(self):
        import urllib2
        url = 'https://cloud.sagemath.com/stats'
        try:
            stats = urllib2.urlopen(url).read()
            self.response.write(stats)
        except:
            self .error(500)

routing = [
    ('/',           MainPage),
    ('/contact',    ContactForm),
    ('/stats',      Stats)
]
app = webapp2.WSGIApplication(routing, debug=DEBUG)
