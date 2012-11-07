#!/usr/bin/python
#coding=utf-8

import unittest
from weibopy.auth import OAuthHandler, BasicAuthHandler
from weibopy.api import API

class SinaAPI(unittest.TestCase):

	consumer_key= "660036463"
	consumer_secret ="e653fec31eca940165c56e04f9a9fcc4"

	def __init__(self):
			""" constructor """

	def getAtt(self, key):
		try:
			return self.obj.__getattribute__(key)
		except Exception, e:
			print e
			return ''

	def getAttValue(self, obj, key):
		try:
			return obj.__getattribute__(key)
		except Exception, e:
			print e
			return ''

	def parseUserInfo(self, user):
		u = {}
		self.obj = user
		u["id"] = self.getAtt("id")
		u["followers_count"] = self.getAtt("followers_count")
		u["statuses_count"] = self.getAtt("statuses_count")
		u["favourites_count"] = self.getAtt("favourites_count")
		u["description"] = self.getAtt("description")
		u["gender"] = self.getAtt("gender")
		u["friends_count"] = self.getAtt("friends_count")
		u["screen_name"] = self.getAtt("screen_name")
		u["profile_image_url"] = self.getAtt("profile_image_url")
		u["created_at"] = self.getAtt("created_at")
		u["location"] = self.getAtt("location")
		u["url"] = self.getAtt("url")
		u["domain"] = self.getAtt("domain")
		return u

	def parseSearchResult(self, line):
		m = {}
		self.obj = line
		m["id"] = self.getAtt("id")
		m["text"] = self.getAtt("text")
		m["from_user_id"] = self.getAtt("from_user_id")
		m["from_user"] = self.getAtt("from_user")
		m["to_user_id"] = self.getAtt("to_user_id")
		m["to_user"] = self.getAtt("to_user")
		m["source"] = self.getAtt("source")
		m["profile_image_url"] = self.getAtt("profile_image_url")
		m["created_at"] = self.getAtt("created_at")
		return m

	def parseUserTimeline(self, line):
		m = {}
		self.obj = line
		m["created_at"] = self.getAtt("created_at")
		m["text"] = self.getAtt("text")
		m["truncated"] = self.getAtt("truncated")
		m["in_reply_to_status_id"] = self.getAtt("in_reply_to_status_id")
		m["in_reply_to_screen_name"] = self.getAtt("in_reply_to_screen_name")
		m["geo"] = self.getAtt("geo")
		m["user"] = self.getAtt("user")
		m["favorited"] = self.getAtt("favorited")
		m["in_reply_to_user_id"] = self.getAtt("in_reply_to_user_id")
		m["created_at"] = self.getAtt("created_at")
		m["id"] = self.getAtt("id")
		m["source"] = self.getAtt("source")
		return m

	def setToken(self, token, tokenSecret):
		self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.setToken(token, tokenSecret)
		self.api = API(self.auth)

	def basicAuth(self, source, username, password):
		self.auth = BasicAuthHandler(username, password)
		self.api = API(self.auth,source=source)

	def auth(self):
		self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
		auth_url = self.auth.get_authorization_url()
		print 'Please authorize: ' + auth_url
		verifier = raw_input('PIN: ').strip()
		self.auth.get_access_token(verifier)
		self.api = API(self.auth)

	def t_sina_public_timeline(self, count=2, page=1):
		timeline = self.api.public_timeline(count=count, page=page)
		for line in timeline:
			self.obj = line
			mid = self.getAtt("id")
			text = self.getAtt("text")
			print "public_timeline---"+ str(mid) +":"+ text

	def t_sina_search_by_user(self, name="", id="", rpp=10, page=1):
		if name or id:
			timeline = self.api.user_timeline(screen_name=name, user_id=id, count=rpp, page=page)
			mlist = []
			for line in timeline:
				mlist.append(self.parseUserTimeline(line))
			return mlist
		else:
			return []

	def t_sina_search_by_keyword(self, keywords, rpp=10, page=1):
		results = self.api.search(q=keywords, rpp=rpp, page=page)
		mlist = []
		for line in results:
			mlist.append(self.parseSearchResult(line))
		return mlist

	def t_sina_search_user_(self, name="", id="", domain="",page=1,rpp=10):
		ulist = []
		if id:
			user = self.api.get_user(user_id=id)
			ulist.append(self.parseUserInfo(user))
			return ulist
		elif domain:
			res_t=rpp
			while(res_t==rpp):
				res_t=0
				users = self.api.search_users(q=domain,sdomain=1,sort=2,page=page,count=rpp)
				for user in users:
					res_t=res_t+1
					us=self.parseUserInfo(user)
					if us['domain']==domain:
						ulist.append(us)
						return ulist
				return ulist
		elif name:
			users = self.api.search_users(q=name,sdomain=0,sort=2,page=page,count=rpp)
			for user in users:
				ulist.append(self.parseUserInfo(user))
			return ulist
		else:
			return []

	def t_sina_get_user_all_friends_(self, rpp=10, id=""):
		ulist = []
		if id:
			res_t=0
			cursor=0
			last_uid=0
			this_last_uid=0
			while(res_t<rpp):
				cursor=cursor+1
				users = self.api.friends(user_id=id,cursor=cursor,count=rpp)
				for user in users:
					this_last_uid=self.parseUserInfo(user)['id']
				if this_last_uid==last_uid:
					break
				else:
					last_uid=this_last_uid
					for user in users:
						res_t=res_t+1
						ulist.append(self.parseUserInfo(user))
		else:
			return []

		return ulist





if __name__ == "__main__":
	test = SinaAPI()
	#AccessToken key Secret
	#test.auth()
	token = "6dbdb9023462c0a07ee5ea16926c549c"
	secret = "94005be8f4ce4038241a3754ebcb7b73"
	test.setToken(token, secret)

	try:
		test.t_sina_public_timeline()
		print "--- public_timeline test OK ---"

		test.t_sina_search_by_keyword('sjtu')
		print "--- t_sina_search_by_keyword test OK ---"

		test.t_sina_search_by_user('zzq889')
		print "--- t_sina_search_by_user(name) test OK ---"

		test.t_sina_search_user_('zzq889')
		print "--- t_sina_search_user_(name) test OK ---"

		test.t_sina_search_user_('11051')
		print "--- t_sina_search_user_(id) test OK ---"

		print "ALL TESTS PASSED. "
	except Exception, e:
		print e
