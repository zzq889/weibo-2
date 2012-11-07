#-*- encoding:utf-8 -*-
import simplejson,base64
from datetime import datetime
from urllib import urlencode
from urllib2 import urlopen, Request

BASE_URL = "http://api.t.sohu.com/"
SEARCH_BY_KEYWORDS = BASE_URL + "statuses/search.json"
SEARCH_BY_USER = BASE_URL + "statuses/user_timeline/$id.json"
SEARCH_FOR_USER = BASE_URL + "users/search.json"
GET_USER_BY_ID = BASE_URL + "users/show/$id.json"
GET_FRIENDS = BASE_URL + "statuses/friends.json"

__user__ = 'gsj987@21cn.com'
__token__ = '312300'

header = {}
basic_auth = base64.encodestring('%s:%s' %(__user__, __token__))[:-1]
header['Authorization'] = 'Basic %s' % basic_auth

def __search_by_keyword__(keywords, page=1):
	url = SEARCH_BY_KEYWORDS + "?%s" %(urlencode({
			'q':keywords, 'page':page}),)
	req = Request(url, headers=header)
	try:
		source = simplejson.loads(urlopen(req).read())['statuses']
	except Exception, e:
		print e
		return []

	return source

def __search_by_user__(id="", name="", page=1):
	if id:
		url = SEARCH_BY_USER.replace('$id',id)
	elif name:
		encoded_name = urlencode({'name':name})[5:]
		url = SEARCH_BY_USER.replace('$id',encoded_name)
	else: return []
	req = Request(url+"?page="+str(page), headers=header)
	return simplejson.loads(urlopen(req).read())

def __search_for_user__(name):
	url = SEARCH_FOR_USER + "?%s" %(urlencode({'q':name}))
	req = Request(url, headers=header)
	return simplejson.loads(urlopen(req).read())

def __get_user_by_id__(id="", name=""):
	if id:
		url = GET_USER_BY_ID.replace('$id',id)
	elif name:
		encoded_name = urlencode({'name':name})[5:]
		url = GET_USER_BY_ID.replace('$id',encoded_name)
	else: return[]

	req = Request(url, headers=header)
	return simplejson.loads(urlopen(req).read())

def __get_user_all_friends__(rpp=10,id=""):
	if not id: return []
	url = GET_FRIENDS + "?id=%s" %(id,)
	page = 1
	count = 0
	friends = []
	while count< rpp:
		req = Request(url+'&page=%d' %(page,), headers=header)
		f_list = simplejson.loads(urlopen(req).read())
		friends += f_list
		count += len(f_list)
		if len(f_list)==0:
			return friends
		page+=1
	return friends


if __name__ == '__main__':
	pass
	#print __search_by_keyword__(keywords="热力追踪")
	#print __search_by_user__(name="冷笑话精选")
	#print __search_for_user__(name="Tony7")
	#print __get_user_by_id__(name="gsj987")
