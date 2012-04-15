__author__ = 'xlzhu'

from google.appengine.ext import db

class VSignImage(db.Model):
    user = db.UserProperty()
    image = db.BlobKey
    geo = db.GeoPtProperty()
