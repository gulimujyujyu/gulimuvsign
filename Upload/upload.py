import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import webapp2
from django.template import loader as django_loader
from django.template import Template

from google.appengine.api import users
################
import urllib

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db
from google.appengine.api.logservice import AppLog

#ours
from data import image_model
from geo import geotypes
import logging

class MainHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload_image')
        #AppLog.message("h")
        user = users.get_current_user()
        if user:
            user_url = users.create_logout_url(self.request.uri)
            user_is_logged_in = True
        else:
            user_url = users.create_login_url(self.request.uri)
            user_is_logged_in = False

        #hello
        template_values = {
            'user_url': user_url,
            'user_is_logged_in': user_is_logged_in,
            'user_obj': user,
            'upload_url': upload_url,
        }

        self.response.out.write(django_loader.render_to_string('upload.html',template_values))

    def post(self):
        upload_url = blobstore.create_upload_url('/upload_image')
        #AppLog.message("h")
        user = users.get_current_user()
        if user:
            user_url = users.create_logout_url(self.request.uri)
            user_is_logged_in = True
        else:
            user_url = users.create_login_url(self.request.uri)
            user_is_logged_in = False

        lon = self.request.get('input_lon');
        lat = self.request.get('input_lat');
        blobkey = self.request.get('image');

        logging.info(lon)
        logging.info(lat)

        geo_info=geotypes.Point(float(lat),float(lon))
        #geo_info = db.GeoPt;
        #geo_info.lat = float(lat);
        #geo_info.lon = float(lon);

        user = users.get_current_user()

        new_vsignimage =image_model.VSignImage(location="%s,%s" % (geo_info.lat, geo_info.lon),user=user,image_key=blobkey)
        #new_vsignimage.user = user
        #new_vsignimage.image = blobkey
        logging.info(geo_info)
        #new_vsignimage.geo = "%s,%s" % (geo_info.lat, geo_info.lon)
        #new_vsignimage.put()
        new_vsignimage.update_location()
        new_vsignimage.put()

        #hello
        template_values = {
            'user_url': user_url,
            'user_is_logged_in': user_is_logged_in,
            'user_obj': user,
            'upload_url': upload_url,
            'upload_is_successful': True
        }

        self.response.out.write(django_loader.render_to_string('upload.html',template_values))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        #AppLog.message(self.request.uri)

        upload_files = self.get_uploads()  # 'file' is file upload field in the form
        logging.info(upload_files)
        blob_info = upload_files[0]

        self.response.out.write(blob_info.key())
        #self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)


################

app = webapp2.WSGIApplication(
    [('/upload', MainHandler),
        ('/upload_image', UploadHandler),
        ('/serve/([^/]+)?', ServeHandler),
    ], debug=True)

