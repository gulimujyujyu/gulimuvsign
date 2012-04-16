__author__ = 'xlzhu'

import hashlib
import hmac
from google.appengine.api import urlfetch
from google.appengine.runtime.apiproxy_errors import OverQuotaError
import json
import urllib
import base64
import logging

MAPS_CLIENT_ID = '906145616468.apps.googleusercontent.com'
MAPS_KEY = 'AIzaSyC9rD4Ly_NR2ltKQ92Ow4wivk-Wdm6va9U'

def get_geocode(address, is_free=True):
    if is_free == False:
        sig, url = make_signed_url('maps.google.com', '/maps/api/geocode/json', [
            (u'address', address),
            (u'sensor', u'false'),
        ], MAPS_CLIENT_ID, MAPS_KEY)
    else:
        sig, url = make_unsigned_url('maps.google.com', '/maps/api/geocode/json', [
            (u'address', address),
            (u'sensor', u'false'),
        ], MAPS_KEY)
    tmp_cnt = urlfetch.fetch(url).content
    #logging.info(tmp_cnt)
    response = json.loads(tmp_cnt)
    if response['status'] == 'OVER_QUERY_LIMIT':
        raise OverQuotaError()
    elif response['status'] == 'ZERO_RESULTS':
        result = None
    elif response['status'] == 'OK':
        result = response['results'][0]
    else:
        raise Exception(response)
    return result

def make_signed_url(domain, path, query, client_id, key):
    query = [(x.encode('utf-8'), y.encode('utf-8')) for x, y in query]
    query.append(('client', client_id))
    path = u'%s?%s' % (path, urllib.urlencode(query))
    sig = base64.urlsafe_b64encode(hmac.new(key, path, hashlib.sha1).digest())
    return sig, u'http://%s%s&signature=%s' % (domain, path, sig)

def make_unsigned_url(domain, path, query, key):
    query = [(x.encode('utf-8'), y.encode('utf-8')) for x, y in query]
    path = u'%s?%s' % (path, urllib.urlencode(query))
    sig = base64.urlsafe_b64encode(hmac.new(key, path, hashlib.sha1).digest())
    return sig, u'http://%s%s' % (domain, path)