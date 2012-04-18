__author__ = 'xlzhu'

# django settings
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# gae routines
import webapp2
from django.template import loader as django_loader
from django.template import Template

# google routines
from google.appengine.api import users
from google.appengine.ext import db

# debug routines
import logging

# db routines
from data import image_model
from geocode import geocoder
from upload import upload

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            user_url = users.create_logout_url(self.request.uri)
            user_is_logged_in = True
        else:
            user_url = users.create_login_url(self.request.uri)
            user_is_logged_in = False

        #randomly assign two images to this user
        results = db.GqlQuery("SELECT * FROM VSignImage LIMIT 2")

        #hello
        template_values = {
            'user_url': user_url,
            'user_is_logged_in': user_is_logged_in,
            'user_obj': user,
            }

        #logging.info(dir(results))

        image_left = None
        image_right = None

        logging.info(results.count())

        if results.count() >= 2:
            image_left = results[0]
            image_right = results[1]

        if results.count() >= 2:
            template_values.update( {'image_left_key': image_left.image_key.key()})
            template_values.update( {'image_right_key': image_right.image_key.key()})


        self.response.out.write(django_loader.render_to_string('label_get.html',template_values))

    def post(self):
        user = users.get_current_user()

        if user:
            user_url = users.create_logout_url(self.request.uri)
            user_is_logged_in = True
        else:
            user_url = users.create_login_url(self.request.uri)
            user_is_logged_in = False

        #randomly assign two images to this user
        results = db.GqlQuery("SELECT * FROM VSignImage LIMIT 2")


        lbb = self.request.get('image_left_bb')
        logging.info(lbb)
        lpts = ('%s' % lbb).split('|');
        logging.info(lpts)
        lx1 = lpts[0]
        ly1 = lpts[1]
        lx2 = lpts[2]
        ly2 = lpts[3]

        rbb = self.request.get('image_right_bb');
        rpts = ('%s' % rbb).split('|');
        rx1 = rpts[0]
        ry1 = rpts[1]
        rx2 = rpts[2]
        ry2 = rpts[3]

        #hello
        template_values = {
            'user_url': user_url,
            'user_is_logged_in': user_is_logged_in,
            'user_obj': user,
            'image_left_key': self.request.get('image_left_key'),
            'image_left_bb': {
                'x1': lx1,
                'x2': lx2,
                'y1': ly1,
                'y2': ly2,
            },
            'image_right_key': self.request.get('image_right_key'),
            'image_right_bb': {
                'x1': rx1,
                'x2': rx2,
                'y1': ry1,
                'y2': ry2,
            },
        }

        self.response.out.write(django_loader.render_to_string('label_post.html',template_values))

app = webapp2.WSGIApplication([('/label', MainPage)],
    debug=True)


