#_*_ coding: utf-8 _*_
# apis about twitter
import simplejson,base64
from datetime import datetime
from urllib import urlencode
from urllib2 import urlopen, Request

BASE_URL = "https://58.64.158.81:10443/twip/o/gsj987/HHTLJE/"
SEARCH_URL = "https://58.64.158.81:10443/twip/o/gsj987/HHTLJE/"
SEARCH_BY_KEYWORDS = SEARCH_URL + "search.json"
SEARCH_BY_USER = BASE_URL + "statuses/user_timeline.json"
SEARCH_FOR_USER = BASE_URL + "users/search.json"
GET_TWEET_BY_ID = BASE_URL + "statuses/show/"
GET_USER_BY_ID = BASE_URL + "users/show.json"
GET_FRIENDS = BASE_URL + "statuses/friends.json"

#__user__ = 'gsj987'
#__token__ = '312300'


header = {}
#basic_auth = base64.encodestring('%s:%s' % (__user__, __token__))[:-1]
#header['Authorization'] = 'Basic %s' % basic_auth

def __search_by_keyword__(keywords,page):
	url_ = SEARCH_BY_KEYWORDS + "?q=%s" %(keywords,)
	if page>1:
		url_ += '&page=%d' %(page,)
	req_ = Request(url_, headers=header)
	try:
		source = simplejson.loads(urlopen(req_).read())['results']
	except Exception,e:
		print e
		return []

	return source


def __search_by_user__(id="", name="", page=1):
	if id:
		url = SEARCH_BY_USER + "?user_id=%s" %(id,)
	elif name:
		url = SEARCH_BY_USER + "?screen_name=%s" %(name,)
	else: return []
	url += "&page=%d" %(page,)

	req = Request(url, headers=header)
	return simplejson.loads(urlopen(req).read())

def __search_for_user__(name):
	url_self = SEARCH_FOR_USER + "?q=%s" %(name)
	req_self = Request(url_self, headers=header)
	return simplejson.loads(urlopen(req_self).read())

def __get_user_by_id__(id="", name=""):
	url = ""
	if id:
		url = GET_USER_BY_ID + "?user_id=%s" %(id,)
	elif name:
		url = GET_USER_BY_ID + "?screen_name=%s" %(name,)
	else: return []

	req = Request(url, headers=header)
	return simplejson.loads(urlopen(req).read())

def __get_user_all_friends__(rpp=10, id=""):
	if not id: return []
	url = GET_FRIENDS +'?user_id=%s' %(id,)
	req = Request(url, headers=header)
	count = 0
	friends = []
	cursor = "-1"
	while count < rpp:
		req = Request(url+'&cursor=%s'%(cursor,), headers=header)
		f_list = simplejson.loads(urlopen(req).read())
		friends += f_list['users']
		cursor = f_list['next_cursor_str']
		count += len(f_list['users'])
		if len(f_list['users']) == 0:
			return friends
	return friends[:rpp]

def __get_tweet_by_id(id="", url=""):
  """通过ID获取某条推的内容

  Args:
    id: tweet的ID
    url: tweet的url

  Returns:
    一个字典，包含tweet内容
  """
  tweet_id = None
  if id:
    tweet_id = id
  elif url:
    tweet_id = url[url.rfind('/')+1:]
  else:
    return None

  url = GET_TWEET_BY_ID + tweet_id + '.json'
  req = Request(url, headers=header)
  r = urlopen(req).read()
  return simplejson.loads(r)

if __name__ == '__main__':
  #print __search_by_keywords__('sjtu')
  #print __search_by_user__(id="9186402")
  #print __search_by_user__(name="gsj987")
  #print __search_for_user__(name="gsj987")
  print __get_tweet_by_id(url="http://twitter.com/Suyutong/status/39242635109613568")
