__author__ = 'xlzhu'

from google.appengine.ext import db
from google.appengine.ext import blobstore

class VSignImage(db.Model):
    user = db.UserProperty()
    image = blobstore.BlobReferenceProperty()
    #lalala = db.StringProperty()
    #geo = db.GeoPtProperty() #TODO
