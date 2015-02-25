#!/usr/bin/env python
import os
import logging
import webapp2
import jinja2

import datetime

YEAR = str(datetime.date.today().year)

GLOBAL_VALS = {
    "year": YEAR,
    "email": "office@sagemath.com",
    "smc": "SageMathCloud",
    "company": "SageMath, Inc.",
    "slogan": "Collaborative Computational Mathematics Online."
}

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


class ContactForm(webapp2.RedirectHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        for k in self.request.arguments():
            logging.info("%s: %s" % (k, self.request.get(k)))


app = webapp2.WSGIApplication([
                                  ('/', MainPage),
                                  ('/contact', ContactForm)
                              ],
                              debug=True)
