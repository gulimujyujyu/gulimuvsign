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

from geo import geotypes
import logging
from django.utils import simplejson

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
            ###
            lat = result['geometry']['location']['lat']
            lon = result['geometry']['location']['lng']
            center = geotypes.Point(float(lat),float(lon))
            logging.info(center)

            #location="%s,%s" % (geo_info.lat, geo_info.lon)
            results = image_model.VSignImage.proximity_fetch(
                image_model.VSignImage.all(),  # Rich query!
                center,  # Or db.GeoPt
                max_results=3,
                max_distance=100000)  #m 80467==Within 50 miles.

            logging.info(results.__getitem__(0))

            public_attrs = image_model.VSignImage.public_attributes()

            results_obj = [
            _merge_dicts({
                'lat': image_result.location.lat,
                'lng': image_result.location.lon,
                'user':image_result.user,
                'image_key':image_result.image_key},
                dict([(attr, getattr(result, attr))
                for attr in public_attrs]))
            for image_result in results]

            logging.info(results_obj)
            simplejson.dumps({'results': results_obj})

            ###
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

