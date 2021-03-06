# django settings
import os
from geocode import geocoder

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# gae routines
import webapp2
from django.template import loader as django_loader

# google routines
from google.appengine.api import users

# db routines
from data import image_model

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
            zoom_level = 2
        else:
            result = None
            zoom_level = 2

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
            zoom_level = 10
        else:
            results = image_model.VSignImage.gql("LIMIT 10")

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
            zoom_level = 2

        #hello
        template_values = {
            'user_url': user_url,
            'user_is_logged_in': user_is_logged_in,
            'user_obj': user,
            'map_center': result,
            'map_result': rslt,
            'zoom_level': zoom_level
        }

        self.response.out.write(django_loader.render_to_string('main.html',template_values))


app = webapp2.WSGIApplication([('/', MainPage)],
                             debug=True)

