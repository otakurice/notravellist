#! /usr/bin/env python3  
#coding=utf-8  
import pandas as pd
import numpy as np
import json, re, io

inf_list = []
add_list = []
hotplace_pd = pd.read_csv('hotplace.csv', index_col=0)
hotplace_np = np.array(hotplace_pd)
inf_list=hotplace_np.tolist()
for li in inf_list:
    li[2] = li[2].split('·')[0] #将excel转为list
top_list = []
name_list = []
k = 1
for li in inf_list[:20]:
    name_list.append(str(li[0]))
    top_list.append(str(int(li[4])))
    k+=1
top_list.reverse()
name_list.reverse()
print('热门景点前20名称：', name_list)
print('热门景点前20销量：', top_list, '\n')

#生成各城市热门景点数量排行榜
for li in inf_list:
    add_list.append(li[2])
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
print('主要城市名称：',add_key)
print('城市对应景点数目：',add_value, '\n')

#生成景点级别
level_list = []
level_5a = []
level_4a = []
level_3a = []
for add in add_key:
    level = []
    i = 0
    while i < len(inf_list):
        if inf_list[i][2]==str(add):
            level_list.append(inf_list[i][1])
        i+=1
    level = set(level_list)
    level_dict = {}
    for item in level:
        level_dict.update({item:level_list.count(item)})
    level_dict.pop('0')
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
print('top20城市名称：',add_key[-20:])
print('3A景区：',level_3a[-20:])
print('4A景区：',level_4a[-20:])
print('5A景区：',level_5a[-20:], '\n')

#生成价格列表
price_list = []
price_key = []
price_value = []
new_add_key = []
for add in add_key:
    price = []
    i = 0
    while i < len(inf_list):
        if inf_list[i][2]==str(add):
            price.append(inf_list[i][3])
        i+=1
    maxprice = max(price)
    minprice = min(price)
    if maxprice == minprice:
        continue
    average = "{:.2f}".format(sum(price)/len(price))
    new_add_key.append(add)
    price_list.append([minprice,maxprice,float(average)])
price_dict = dict(zip(new_add_key,price_list))
s_price_dict = sorted(price_dict.items(), key=lambda d:d[1][1],reverse = True)
for value in s_price_dict:
    price_key.append(value[0])
    price_value.append(value[1])
print('各省名称：',price_key)
print('各省对应景点价格：',price_value)

def datatojson(sightlist):  #直接生成json数据
    bjsonlist = []
    ejsonlist1 = []
    ejsonlist2 = []
    num = 1
    for l in sightlist:
        json_geo = {}
        p = '(.*?),(.*?)$'
        geo = re.findall(p,l[7])[0]
        json_geo['lat'] = geo[1]
        json_geo['count'] = l[4]/100
        json_geo['lng'] = geo[0]
        bjsonlist.append(json_geo)
#        print('正在生成第', str(num), '个景点的经纬度')
        ejson1 = {l[0] : [geo[0],geo[1]]}
        ejsonlist1 = dict(ejsonlist1,**ejson1)
        ejson2 = {'name' : l[0],'value' : l[4]/100}
        ejsonlist2.append(ejson2)
        num +=1
    bjsonlist =json.dumps(bjsonlist)
    ejsonlist1 = json.dumps(ejsonlist1, ensure_ascii=False)
    ejsonlist2 = json.dumps(ejsonlist2, ensure_ascii=False)
    with open('./points.json',"w") as f:
        f.write(bjsonlist)
    with open('./geoCoordMap.json',"w", encoding='utf-8') as f:
        f.write(ejsonlist1)
    with open('./data.json',"w", encoding='utf-8') as f:
        f.write(ejsonlist2)

datatojson(inf_list)