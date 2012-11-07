#!/usr/bin/python
#-*- encoding: utf-8 -*-


import api
#mc_list = ['qq','sina','twitter','sohu']
mc_list = ['qq']
by_keyword = api.t_search_by_keyword(
		mc_list=mc_list,
		keywords="姚晨",
		page=1
	)


by_user = api.t_search_by_user(
		mc_list = mc_list,
		name = 'gsj987',
	)

for_user = api.t_search_user(
		mc_list = mc_list,
		name = '冷笑话精选',
	)

get_friends = api.t_get_user_all_friends(
		mc_list = mc_list,
		id = '9186402',
	)
#sina_for_user = api.t_sina_search_user(
#		name = '钢丝君',
#	)

#sina_by_user = api.t_sina_search_by_user(
#		name = 'zzq889',
#	)
#sina_by_keyword = api.t_sina_search_by_keyword(
#		keywords='sjtu',
#	)

#总的输出
print "="*10, "关键词", "="*10
for mcs in by_keyword:
	for t in mcs:
		print repr(t.__dump__())

print "="*10, "用户", "="*10
for mcs in by_user:
	for t in mcs:
		print repr(t.__dump__())

print "="*10, "搜用户", "="*10
for mcs in for_user:
	for u in mcs:
		print repr(u.__dump__())

print "="*10, "找朋友", "="*10
for mcs in get_friends:
	for u in mcs:
		print repr(u.__dump__())
#sina
#for t in sina_by_keyword:
#	print repr(t.__dump__())

#for t in sina_by_user:
#	print repr(t.__dump__())

#for u in sina_for_user:
#	print repr(t.__dump__())

