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
from google.appengine.api.logservice import AppLog

#ours
from data import image_model

class MainHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload_one')
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

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        #AppLog.message(self.request.uri)

        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form

        user = users.get_current_user()
        blob_info = upload_files[0]

        new_vsignimage = image_model.VSignImage()
        new_vsignimage.user = user
        new_vsignimage.image = blob_info.key()
        new_vsignimage.put()

        self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)


################

app = webapp2.WSGIApplication(
    [('/upload', MainHandler),
        ('/upload_one', UploadHandler),
        ('/serve/([^/]+)?', ServeHandler),
    ], debug=True)

