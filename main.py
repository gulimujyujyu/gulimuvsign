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
import json

def _merge_dicts(*args):
    """Merges dictionaries right to left. Has side effects for each argument."""
    return reduce(lambda d, s: d.update(s) or d, args)

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


            #simplejson.dumps({'results': results_obj})

            rslt=[]
            for i in results:
                rslt.append({
                    'lat': i.location.lat,
                    'lng': i.location.lon,
                    'user':{
                        'name':i.user.user_id(),
                        'email':i.user.email()
                    },
                    'image_key':"%s" % i.image_key.key()})
            ###
            logging.info(rslt)
            map_query = json.dumps(rslt)
            logging.info(map_query)
            #map_query='a'
        else:
            map_query = None

        #hello
        template_values = {
            'user_url': user_url,
            'user_is_logged_in': user_is_logged_in,
            'user_obj': user,
            'map_center': result,
            'map_result': rslt
        }

        self.response.out.write(django_loader.render_to_string('main.html',template_values))


app = webapp2.WSGIApplication([('/', MainPage)],
                             debug=True)

