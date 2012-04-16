# django settings
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# gae routines
import webapp2
from django.template import loader as django_loader
from django.template import Template

# google routines
from google.appengine.api import users

# db routines
from data import image_model
from geocode import geocoder
from Upload import upload

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            user_url = users.create_logout_url(self.request.uri)
            user_is_logged_in = True
        else:
            user_url = users.create_login_url(self.request.uri)
            user_is_logged_in = False


        address = self.request.get('address')
        if address:
            result = geocoder.get_geocode(address)
        else:
            result = None

        if result:
            map_query = 'a'
        else:
            map_query = None

        #hello
        template_values = {
            'user_url': user_url,
            'user_is_logged_in': user_is_logged_in,
            'user_obj': user,
            'map_center': result,
            'map_result': map_query
        }

        self.response.out.write(django_loader.render_to_string('main.html',template_values))


app = webapp2.WSGIApplication([('/', MainPage)],
                             debug=True)

