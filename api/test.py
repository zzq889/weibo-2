#!/usr/bin/python
#-*- encoding: utf-8 -*-


import apis

by_keyword = apis.t_search_by_keyword(
		mc_list=['sina','twitter',],
		keywords="热力追踪",
		page=1
	)

by_user = apis.t_search_by_user(
		mc_list = ['sina','twitter',],
		name = 'zzq889',
	)

for_user = apis.t_search_user(
		mc_list = ['sina','twitter',],
		name = '钢丝君',
	)

for mcs in by_keyword:
	for t in mcs:
		print repr(t.__dump__())

for mcs in by_user:
	for t in mcs:
		print repr(t.__dump__())

for mcs in for_user:
	for u in mcs:
		print repr(u.__dump__())
