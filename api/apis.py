#_*_ coding: utf-8 _*_
# the apis

import re
from datetime import datetime
import models, twitter, sina, sohu, qq


by_keyword_funcs = {
    'sina':
    	lambda *args,**kwargs:
    		t_sina_search_by_keyword(*args, **kwargs),
		'twitter':
			lambda *args, **kwargs:
				t_twitter_search_by_keyword(*args, **kwargs),
		'sohu':
			lambda *args, **kwargs:
				t_sohu_search_by_keyword(*args, **kwargs),
		'qq':
			lambda *args, **kwargs:
				t_qq_search_by_keyword(*args, **kwargs),
	}

by_user_funcs = {
		'sina':
			lambda *args, **kwargs:
				t_sina_search_by_user(*args, **kwargs),
		'twitter':
			lambda *args, **kwargs:
				t_twitter_search_by_user(*args, **kwargs),
		'sohu':
			lambda *args, **kwargs:
				t_sohu_search_by_user(*args, **kwargs),
		'qq':
			lambda *args, **kwargs:
				t_qq_search_by_user(*args, **kwargs),
	}

for_user_funcs = {
		'sina':
			lambda *args, **kwargs:
				t_sina_search_user(*args, **kwargs),
		'twitter':
			lambda *args, **kwargs:
				t_twitter_search_user(*args, **kwargs),
		'sohu':
			lambda *args, **kwargs:
				t_sohu_search_user(*args, **kwargs),
		'qq':
			lambda *args, **kwargs:
				t_qq_search_user(*args, **kwargs),
	}

get_friends_funcs = {
		'sina':
			lambda *args, **kwargs:
				t_sina_get_user_all_friends(*args, **kwargs),
		'twitter':
			lambda *args, **kwargs:
				t_twitter_get_user_all_friends(*args, **kwargs),
		'sohu':
			lambda *args, **kwargs:
				t_sohu_get_user_all_friends(*args, **kwargs),
		'qq':
			lambda *args, **kwargs:
				t_qq_get_user_all_friends(*args, **kwargs),
	}

def __get_links__(text):
	return re.findall(r'(http://[a-zA-Z0-9/_\-\.]+)\s?',text)
def __get_mentions__(text):
	return re.findall(r'@([a-zA-Z0-9_\-]+)\s', text)
def __remove_utf_offset(time_str):
  offset = re.findall(r'\+\d\d\d\d', time_str)
  if offset:
    return time_str.replace(offset[0], '').strip()
  return time_str.strip()

# main
def __t_search(mc_list=[],func_list={}, *args, **kwargs):
	results = []
	for mc_key in mc_list:
		if func_list[mc_key]:
			results.append(func_list[mc_key](*args,**kwargs))
	return results

def t_search_by_keyword(mc_list, keywords, page=1):
	return __t_search(
			mc_list = mc_list,
			func_list = by_keyword_funcs,
			keywords = keywords,
			page = page
		)

def t_search_by_user(mc_list, id="", name="", page=1):
	return __t_search(
			mc_list = mc_list,
			func_list = by_user_funcs,
			id = id,
			name = name,
			page = page,
		)

def t_search_user(mc_list, id="", name=""):
	return __t_search(
			mc_list = mc_list,
			func_list = for_user_funcs,
			id = id,
			name = name,
		)

def t_get_user_all_friends(mc_list, id="", rpp=10):
	return __t_search(
			mc_list = mc_list,
			func_list = get_friends_funcs,
			id = id,
			rpp = rpp,
		)

# sina
def __get_sina_api__():
	w = sina.SinaAPI()
	token = "6dbdb9023462c0a07ee5ea16926c549c"
	secret = "94005be8f4ce4038241a3754ebcb7b73"
	w.setToken(token, secret)

	return w

def t_sina_search_by_keyword(keywords="", page=1,rpp=10):
	_api = __get_sina_api__()
	results = _api.t_sina_search_by_keyword(keywords, page=page,rpp=rpp)
	res = []
	for result in results:
		res.append(models.TInfo(
			src = 'sina',
			id = result.get('from_user_id'),
			name = result.get("from_user"),
			id_follow = [result.get("to_user").encode('utf-8'),],
			home_id = "http://t.sina.com.cn/%s" %(str(result.get('from_user_id')),),
			weibo_id = result.get('id'),
			info = result.get('text'),
			link = __get_links__(result.get('text')+' '),
			time = result.get('created_at').isoformat().replace('T',' '),
			geo_info = result.get('geo'),
		))
	return res

def t_sina_search_by_user(id="", name="", page=1,rpp=10):
	_api = __get_sina_api__()
	results = _api.t_sina_search_by_user(id=id, name=name, page=page,rpp=rpp)
	res = []
	for result in results:
		res.append(models.TInfo(
			src = 'sina',
			id = result.get("user").id,
			id_follow = [result.get('in_reply_to_screen_name').encode("utf-8"),],
			name = result.get("user").name,
			home_id = "http://t.sina.com.cn/%s" %(str(result.get('user').id),),
			weibo_id = result.get("id"),
			info = result.get("text"),
			link = __get_links__(result.get("text")+' '),
			time = result.get('created_at').isoformat().replace('T',' '),
			get_info = result.get('geo'),
		))
	return res

def t_sina_search_user(id="",name="",domain="",page=1,rpp=10):
	_api = __get_sina_api__()
	results = _api.t_sina_search_user_(name=name, id=id,domain=domain,page=page,rpp=rpp)
	res = []
	for result in results:
		res.append(models.UserInfo(
			src = "sina",
			id = result.get('id'),
			name = result.get('screen_name'),
			home_id = "http://t.sina.com.cn/%s" %(str(result.get('id')),),
			fans = result.get('followers_count','0'),
			friends = result.get("friends_count",'0'),
			image = result.get('profile_image_url'),
			url = result.get('url'),
			domain = result.get('domain'),
		))
	return res

def t_sina_get_user_all_friends(rpp=10,id=""):
	_api = __get_sina_api__()
	results = _api.t_sina_get_user_all_friends_(rpp=rpp,id=id)
	res = []
	for result in results:
		res.append(models.UserInfo(
			src = "sina",
			id = result.get('id'),
			name = result.get('screen_name'),
			home_id = "http://t.sina.com.cn/%s" %(str(result.get('id')),),
			fans = result.get('followers_count','0'),
			friends = result.get('friends_count','0'),
			image = result.get('profile_image_url'),
			url = result.get('url'),
			domain = result.get('domain'),
		))
	return res

# twitter

def t_twitter_search_by_keyword(keywords, page=1):
	results = twitter.__search_by_keyword__(keywords,page)
	res = []
	for r in results:
		user_id = r.get('from_user_id')
		user_screen_name = r.get("from_user")
		user_screen_name_in_reply_to = __get_mentions__(r.get("text")+' ')
		user_home = "http://www.twitter.com/%s" %(user_screen_name)
		links = __get_links__(r.get('text')+' ')
		created_at = __remove_utf_offset(r.get('created_at'))
		time = datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S')
		time = time.isoformat().replace('T', ' ')
		res.append(models.TInfo(
			src = 'twitter',
			id = user_id,
			weibo_id = r.get('id'),
			id_follow = user_screen_name_in_reply_to,
			name = user_screen_name,
			home_id = user_home,
			info = r.get('text'),
			link = links,
			time = time,
			geo_info = r.get('geo'),
		))
	return res

def t_twitter_search_by_user(id="", name="", page=1):
	results = twitter.__search_by_user__(id,name, page)
	res = []
	for r in results:
		user = r.get('user')
		user_screen_name_in_reply_to = __get_mentions__(r.get("text")+' ')
		user_home = "http://www.twitter.com/%s" %(user.get('screen_name'))
		links = __get_links__(r.get('text')+' ')
		#time = datetime.strptime(r.get('created_at'), '%a, %d %b %H:%M:%S %z %Y')
		time = r.get('created_at')
		res.append(models.TInfo(
			src = 'twitter',
			id = user.get('id'),
			weibo_id = r.get('id'),
			id_follow = user_screen_name_in_reply_to,
			name = user.get("screen_name"),
			home_id = user_home,
			info = r.get('text'),
			link = links,
			time = time,
			get_info = r.get('get'),
		))
	return res

def t_twitter_search_user(id="", name=""):
	result = []
	if id:
		result = [twitter.__get_user_by_id__(id=id, name=name),]
	elif name:
		result = twitter.__search_for_user__(name=name)
	if not result: return []
	res = []
	for user in result:
		res.append(models.UserInfo(
			src = "twitter",
			id = user.get('id'),
			name = user.get("screen_name"),
			home_id = "http://www.twitter.com/%s" %(user.get('screen_name')),
			fans = user.get('followers_count'),
			friends = user.get('friends_count'),
			image = user.get('profile_image_url'),
		))
	return res

def t_twitter_get_user_all_friends(rpp=10,id=""):
	results = twitter.__get_user_all_friends__(rpp=rpp,id=id)
	res = []
	for result in results:
		res.append(models.UserInfo(
			src = "twitter",
			id = result.get('id'),
			name = result.get('screen_name'),
			home_id = "http://www.twitter.com/%s" %(str(result.get('screen_name')),),
			fans = result.get('followers_count','0'),
			friends = result.get('friends_count','0'),
			image = result.get('profile_image_url'),
		))
	return res

#sohu

def twitter_get_tinfo_by_weibourl(id="", url=""):
  """通过url或ID返回tinfo数据

  Args:
    id: tweet的ID
    url: tweet的url

  Returns:
    一个TInfo，包含微博数据
  """
  result = twitter.__get_tweet_by_id(id=id, url=url)
  created_at = result.get('created_at')
  offset=re.findall(r'\+\d\d\d\d', created_at)[0]
  time = datetime.strptime(created_at.replace(offset, ''), "%a %b %d %H:%M:%S %Y")


  return [models.TInfo(
      src='twitter',
      id=result['user'].get('id'),
      weibo_id=result.get('id'),
      name=result['user'].get('screen_name'),
      id_follow=[result.get('in_reply_to_screen_name'),],
      home_id="http://www.twitter.com/%s" %(result['user'].get('screen_name'),),
      info=result.get('text'),
      link=__get_links__(result.get('text')+' '),
      time=time.isoformat().replace('T', ''),
      geo_info=result.get('geo'),
    ),]


def t_sohu_search_by_keyword(keywords, page=1):
	results = sohu.__search_by_keyword__(keywords, page)
	res = []
	for r in results:
		created_at = __remove_utf_offset(r.get('created_at'))
		time = datetime.strptime(created_at, '%a %b %d %H:%M:%S %Y')
		time = time.isoformat().replace('T',' ')

		res.append(models.TInfo(
			src = "sohu",
			id = r['user'].get('id'),
			name = r['user'].get('screen_name'),
			home_id = 'http://t.sohu.com/u/%s' %(r['user']['id'],),
			id_follow = __get_mentions__(r.get('text')+' '),
			weibo_id = r.get('id'),
			info = r['text'],
			link = __get_links__(r.get('text')+' '),
			time = time,
			geo_info = r.get("geo"),
		))
	return res

def t_sohu_search_by_user(id="", name="", page=1):
	results = sohu.__search_by_user__(id, name, page)
	res = []
	for r in results:
		created_at = __remove_utf_offset(r.get('created_at'))
		time = datetime.strptime(created_at, '%a %b %d %H:%M:%S %Y')
		time = time.isoformat().replace('T',' ')
		res.append(models.TInfo(
			src = "sohu",
			id = r['user'].get('id'),
			name = r['user'].get('screen_name'),
			home_id = 'http://t.sohu.com/u/%s' %(r['user']['id'],),
			weibo_id = r.get('id'),
			id_follow = __get_mentions__(r.get('text')+' '),
			info = r['text'],
			link = __get_links__(r.get('text')+' '),
			time = time,
			geo_info = r.get("geo"),
		))
	return res

def t_sohu_search_user(id="", name=""):
	results = []
	if id:
		results = [sohu.__get_user_by_id__(id),]
	elif name:
		results = sohu.__search_for_user__(name)
	res = []
	for r in results:
		res.append(models.UserInfo(
			src = "sohu",
			id = r.get("id"),
			name = r.get("screen_name"),
			home_id = "http://t.sohu.com/u/%s" %(r.get('id')),
			fans = r.get('followers_count'),
			friends = r.get('friends_count'),
			image = r.get('profile_image_url'),

		))
	return res

def t_sohu_get_user_all_friends(rpp=10,id=""):
	results = sohu.__get_user_all_friends__(rpp=rpp,id=id)
	res = []
	for result in results:
		res.append(models.UserInfo(
			src = "sohu",
			id = result.get('id'),
			name = result.get('screen_name'),
			home_id = "http://t.sohu.com/u/%s" %(result.get('id')),
			fans = result.get('followers_count','0'),
			friends = result.get('friends_count','0'),
			image = result.get('profile_image_url'),
		))
	return res
# qq
def __get_qq_api__():
	return qq.qqAPI()

def t_qq_search_by_keyword(keywords, page=1):
	_api = __get_qq_api__()
	results = _api.t_qq_search_by_keyword(keywords, page)
	res = []
	for r in results:
		res.append(models.TInfo(
			src = "qq",
			id = r.get('uid'),
			id_follow = __get_mentions__(r.get('text')+' '),
			name = r.get('name'),
			home_id = "http://t.qq.com/%s" %(r.get('name')),
			weibo_id = r.get('id'),
			info = r.get('text'),
			link = __get_links__(r.get("text")+' '),
			time = datetime.fromtimestamp(int(r.get('timestamp'))).isoformat().replace('T', ' '),
			geo_info = r.get('geo'),
		))
	return res

def t_qq_search_by_user(id="", name="", page=1):
	_api = __get_qq_api__()
	results = _api.t_qq_search_by_user(id=id, name=name, page=page)
	res = []
	for r in results:
		res.append(models.TInfo(
			src = "qq",
			id = r.get('uid'),
			id_follow = __get_mentions__(r.get('text')+' '),
			name = r.get('name'),
			home_id = "http://t.qq.com/%s" %(r.get('name')),
			weibo_id = r.get('id'),
			info = r.get("text"),
			link = __get_links__(r.get("text")+' '),
			time = datetime.fromtimestamp(int(r.get('timestamp'))).isoformat().replace('T', ' '),
			geo_info = r.get('geo'),
		))
	return res

def t_qq_search_user(id="", name=""):
	_api = __get_qq_api__()
	results = _api.t_qq_search_user(id=id, keyword=name)
	res = []
	for r in results:
		res.append(models.UserInfo(
			src = "qq",
			id = r.get('uid'),
			name = r.get('name'),
			home_id = "http://t.qq.com/%s" %(r.get('name'),),
			fans = r.get('fansnum'),
			friends = r.get('idolnum'),
			image = r.get('head'),
		))
	return res

def t_qq_get_user_all_friends(rpp=10, id=""):
	_api = __get_qq_api__()
	results = _api.t_qq_get_user_all_friends(rpp=rpp,id=id)
	res = []
	for r in results:
		res.append(models.UserInfo(
			src = "qq",
			id = r.get('uid'),
			name = r.get("name"),
			home_id = "http://t.qq.com/%s" %(r.get('name')),
			fans = r.get('fansnum'),
			friends = r.get('idolnum'),
			image = r.get('head'),
		))
	return res

if __name__ == '__main__':
	for t in t_search_user(['twitter',],name="gsj987"):
		print repr(t.__dump__())
