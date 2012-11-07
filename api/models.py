#the models of weibo info


class TInfo(object):
	"""
	the info of weibo.
	src:			the source
	id:				the author's id
	id_follow:		the ids replying to
	name:			the screen_name of the author
	home_id:		the page of the author
	weibo_id:		the id of the weibo
	info:			the content of the weibo
	link:           the	links in the content of weibo
	time:			the time post this weibo
	geo_info:		the geo infomations
	"""

	def __init__(self, **kwargs):
		self.src = kwargs.get('src','unknown')
		self.id = str(kwargs.get('id','no_id'))
		self.id_follow = [str(id_f) for id_f in kwargs.get('id_follow')]
		self.name = kwargs.get('name')
		self.home_id = str(kwargs.get('home_id'))
		self.weibo_id = str(kwargs.get('weibo_id','no_id'))
		self.info = kwargs.get('info')
		self.link = [l for l in kwargs.get('link')]
		self.time = kwargs.get('time')
		self.geo_info = kwargs.get('geo_info')

	def __dump__(self):
		return {
				'src': self.src,
				'id': self.id,
				'id_follow': self.id_follow,
				'name': self.name,
				'home_id': self.home_id,
				'weibo_id': self.weibo_id,
				'info': self.info,
				'link': self.link,
				'time': self.time,
				'geo_info': self.geo_info,
			}

class UserInfo(object):
	"""
	the info of the user
	src:			the source
	id:				the id of this user
	name:			the screen_name of this user
	home_id:		the page of this user
	fans:			the counts of current user's fans
	friends:		the counts of current user's friends
	image:			the url of current user's avatar
	"""

	def __init__(self, **kwargs):
		self.src = kwargs.get('src','unknown')
		self.id = str(kwargs.get('id','no_id'))
		self.name = kwargs.get('name')
		self.home_id = str(kwargs.get('home_id'))
		self.fans = int(kwargs.get('fans'))
		self.friends = int(kwargs.get('friends'))
		self.image = kwargs.get('image')
		self.domain = kwargs.get('domain')
		self.url = kwargs.get('url')

	def __dump__(self):
		return {
				'src': self.src,
				'id': self.id,
				'name': self.name,
				'home_id': self.home_id,
				'fans': self.fans,
				'friends': self.friends,
				'image': self.image,
			}

