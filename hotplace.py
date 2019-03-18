#!/usr/bin/env python3
#_*_ coding: utf-8_*_
import time,requests, re #time用于延时，requests用于请求网页数据，json转换json数据格式，re正则
from lxml import etree #解析xpath网页结构
import pandas as pd #处理表格进行数据分析

def getPage(url):#获取链接中的网页内容
    # 网络请求时需要包含较为完整的headers(请求头)
    # 这里的headers就是requests header的内容
    # 除了cookie 和 user-agent其他都和我的电脑一样
    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection':'keep-alive',
        'cookie':'填写cookies',
        'Host':'piao.qunar.com',
        'Referer':'http://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%'
                  'A8%E6%99%AF%E7%82%B9&region=&from=mpl_search_suggest',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                     ' (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    try:
        page = requests.get(url,headers = headers) # 这里是请求网页数据了
        return page
    except Exception as e:
        print(str(e))

def getList():
    place = '热门景点'
    url = 'http://piao.qunar.com/ticket/list.htm?keyword='+ place +'&region=&from=mpl_search_suggest&page={}'
    i = 1
    sightlist = []
    while i < 150:
        page = getPage(url.format(i)) #这里调用了getPage函数获取了网页数据
        selector = etree.HTML(page.text)
        print('正在爬取第', str(i), '页景点信息')
        i += 1
        informations = selector.xpath('//div[@class="result_list"]/div')
        for inf in informations: #获取必要信息
            sight_name = inf.xpath('./div/div/h3/a/text()')[0]
            sight_level = inf.xpath('.//span[@class="level"]/text()')
            if len(sight_level):
                sight_level = sight_level[0].replace('景区','')
            else:
                sight_level = 0
            sight_area = inf.xpath('.//span[@class="area"]/a/text()')[0]
            print(sight_area)
            sight_hot = inf.xpath('.//span[@class="product_star_level"]//span/text()')[0].replace('热度 ','')
            sight_add = inf.xpath('.//p[@class="address color999"]/span/text()')[0]
            sight_add = re.sub('地址：|（.*?）|\(.*?\)|，.*?$|\/.*?$','',str(sight_add))
            sight_slogen = inf.xpath('.//div[@class="intro color999"]/text()')[0]
            sight_price = inf.xpath('.//span[@class="sight_item_price"]/em/text()')
            if len(sight_price):
                sight_price = sight_price[0]
            else:
                i = 0
                break
            sight_soldnum = inf.xpath('.//span[@class="hot_num"]/text()')[0]
            sight_point = inf.xpath('./@data-point')[0]
            sight_url = inf.xpath('.//h3/a[@class="name"]/@href')[0]
            sightlist.append([sight_name,sight_level,sight_area,float(sight_price),int(sight_soldnum),float(sight_hot),sight_add.replace('地址：',''),sight_point,sight_slogen,sight_url])
        time.sleep(10)
    return sightlist

def listToExcel(list,name):
    df = pd.DataFrame(list,columns=['景点名称','级别','所在区域','起步价','销售量','热度','地址','经纬度','标语','详情网址'])
    df.to_csv(name + ".csv", sep=',')

def main():
    sightlist = getList() # main后第一个运行getList()
    listToExcel(sightlist,'hotplace')

if __name__=='__main__': # 代码是从main函数开始的
	main()