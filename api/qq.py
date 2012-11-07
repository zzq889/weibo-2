#!/usr/bin/python
#_*_ encoding: utf-8 _*_

import simplejson
import oauth
import time
import urllib
import urllib2

class qqAPI():
  # Set up instances of our Token and Consumer. The Consumer.key and
  # Consumer.secret are given to you by the API provider. The Token.key and
  # Token.secret is given to you after a three-legged authentication.
  token = oauth.OAuthToken(key="3cb60d1596e64c16aa6cf634a9b75a53", secret="42d1c6ff9427506e5d00790f8b71a99e")
  consumer = oauth.OAuthConsumer(key="17ec57fbcb1946d686b5e78a7abf53ef", secret="963d67431c16ef144e73c49005ebd677")

  API_ROOT = "http://open.t.qq.com/api"

  def __init__(self):
    """ constructor """

  def access_response(self, RESOURCE_URL, parameters):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=self.token, http_method='GET', http_url=RESOURCE_URL, parameters=parameters)
    signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()
    oauth_request.sign_request(signature_method_hmac_sha1, self.consumer, self.token)

    req = urllib2.Request(RESOURCE_URL +'?'+ urllib.urlencode(oauth_request.parameters))
    response = urllib2.urlopen(req)
    return response.read()

  def t_qq_search_by_keyword(self, keyword="", page=1):
    RESOURCE_URL = self.API_ROOT + "/search/t"
    parameters = {
      'format': 'json',
      'keyword': keyword,
      'pagesize': 20,
      'page': page
    }
    try:
      res = simplejson.loads((self.access_response(RESOURCE_URL, parameters)))
      return res['data']['info']
    except Exception,e:
      print "Error: " ,res
      return []



  def t_qq_search_by_user(self, name="", id="",page=1):
    RESOURCE_URL = self.API_ROOT + "/statuses/user_timeline"
    parameters = {
      'format': 'json',
      'name': name,
      'reqnum': 20,
      'pageflag': page-1,
      'pagetime': 0
    }
    try:
      res = simplejson.loads((self.access_response(RESOURCE_URL, parameters)))
      return res['data']['info']
    except Exception,e:
      print "Error: " ,res
      return []

  def t_qq_search_user(self, id="", keyword=""):
    if id: return []
    RESOURCE_URL = self.API_ROOT + "/search/user"
    parameters = {
      'format': 'json',
      'keyword': keyword,
      'pagesize': 10,
      'page': 1
    }
    try:
      res = simplejson.loads(self.access_response(RESOURCE_URL, parameters))
      return res['data']['info']
    except Exception,e:
      print res
      return []

  def t_qq_get_user_all_friends(self, rpp=10, id=""):
    RESOURCE_URL = self.API_ROOT + "/friends/user_fanslist"
    parameters = {
      'format': 'json',
      'reqnum': rpp,
      'startindex': 0,
      'name': id
    }
    try:
      res = simplejson.loads((self.access_response(RESOURCE_URL, parameters)))
      return res['data']['info']
    except Exception,e:
      print "Error: " ,res
      return []


if __name__ == '__main__':
  test = qqAPI()
  try:
    test.t_qq_search_by_keyword('sjtu')
    print "--- t_qq_search_by_keyword test OK ---"
    test.t_qq_search_by_user('zzq889')
    print "--- t_qq_search_by_user(name) test OK ---"
    test.t_qq_search_user('zzq889@gmail.com')
    print "--- t_qq_search_user_(name) test OK ---"
    test.t_qq_search_user('special')
    print "--- t_qq_search_user_(id) test OK ---"

    print "All tests finished with status 0. "
  except Exception, e:
    print e
