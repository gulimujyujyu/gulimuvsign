__author__ = 'Xiaoyang'

from google.appengine.ext import db

from geo.geomodel import GeoModel
from google.appengine.ext import blobstore

class VSignImage(GeoModel):
    user = db.UserProperty()
    image_key = blobstore.BlobReferenceProperty()

    @staticmethod
    def public_attributes():
    #Returns a set of simple attributes on entities."""
        return [ 'user','image_key']

    def _get_latitude(self):
        return self.location.lat if self.location else None

    def _set_latitude(self, lat):
        if not self.location:
            self.location = db.GeoPt()

        self.location.lat = lat

    latitude = property(_get_latitude, _set_latitude)

    def _get_longitude(self):
        return self.location.lon if self.location else None

    def _set_longitude(self, lon):
        if not self.location:
            self.location = db.GeoPt()

        self.location.lon = lon

    longitude = property(_get_longitude, _set_longitude)
