#! /usr/bin/env python  
#coding=utf-8  
import xlrd
import operator

worksheet = xlrd.open_workbook(u'热门景点景点信息.xlsx')
sheet_names= worksheet.sheet_names()
inf_list = []
add_list = []
for sheet_name in sheet_names:
	sheet1 = worksheet.sheet_by_name(sheet_name)
	#获取第二列内容，输出主要城市热门景点排行榜
	i = 0
	while i < 4485:#4485:
		rows = sheet1.row_values(i)
		i+=1
		inf_list.append(rows)
	del inf_list[0]
	for li in inf_list:
		li[3] = li[3].split('·')[0] #将excel转为list

	j = 0
	list = []
	top_list = []
	name_list = []
	while j < 21:
		rows = sheet1.row_values(j)
		j+=1
		list.append(rows)
	del list[0]
	k = 1
	for li in list:
		top_list.append(str(li[1]))#'“' + str(li[1]) + '”销量：' + str(int(li[5])))
		name_list.append(str(int(li[5])))
		k+=1
	top_list.reverse()
	name_list.reverse()
	print(top_list)
	print(name_list)

	#生成各城市热门景点数量排行榜
	for li in inf_list:
		add_list.append(li[3])
	add_key = []
	add_value = []
	add = set(add_list)
	add_dict = {}
	for item in add:
		add_dict.update({item:add_list.count(item)})
	s_add_dict = sorted(add_dict.items(), key=lambda d:d[1])
	for value in s_add_dict:
		add_key.append(value[0])
		add_value.append(value[1])
	print(add_key)
	print(add_value)

	#生成价格列表
	price_list = []
	price_key = []
	price_value = []
	for add in add_key:
		price = []
		i = 0
		while i < 4484:
			if inf_list[i][3]==str(add):
				price.append(inf_list[i][4])
			i+=1
		maxprice = max(price)
		minprice = min(price)
		average = "{:.2f}".format(sum(price)/len(price))
		price_list.append([minprice,maxprice,average])
	price_dict = dict(zip(add_key,price_list))
	s_price_dict = sorted(price_dict.items(), key=lambda d:d[1][1],reverse = True)
	for value in s_price_dict:
		price_key.append(value[0])
		price_value.append(value[1])
	print(price_key)
	print(price_value)

	#生成景点级别
	level_list = []
	level_5a = []
	level_4a = []
	level_3a = []
	for add in add_key:
		level = []
		i = 0
		while i < 4484:
			if inf_list[i][3]==str(add):
				level_list.append(inf_list[i][2])
			i+=1
		level = set(level_list)
		level_dict = {}
		for item in level:
			level_dict.update({item:level_list.count(item)})
		level_dict.pop(0.0)
		try:
			level_5a.append(level_dict['5A'])
		except Exception as e:
			level_5a.append('0')
		try:
			level_4a.append(level_dict['4A'])
		except Exception as e:
			level_4a.append('0')
		try:
			level_3a.append(level_dict['3A'])
		except Exception as e:
			level_3a.append('0')
	print(level_5a)
	print(level_4a)
	print(level_3a)