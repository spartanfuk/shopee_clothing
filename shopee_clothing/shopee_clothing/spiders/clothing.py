# -*- coding: utf-8 -*-
import scrapy
import re
import time
from shopee_clothing.items import ShopeeClothingItem
import json

# class SfwSpider(RedisSpider):
class SPSpider(scrapy.Spider):
    name = 'clothing'
    allowed_domains = ['my.xiapibuy.com']
    start_urls = ["https://my.xiapibuy.com/api/v2/search_items/?by=sales&limit=50&match_id=17&newest=0&order=desc&page_type=search"]
    # redis_key = "shopee_clothing:start_urls"

    def parse(self, response):
        # newset = 0  # 页数 * 50
        for page_number in range(0, 100):  # 页数
            url = "https://my.xiapibuy.com/api/v2/search_items/?by=sales&limit=50&match_id=17&newest={}&order=desc&page_type=search".format(
                page_number*50)  # newest += 50
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        # print(response)
        print('=' * 50)
        print(response.url)
        print('=' * 50)
        url_detail = json.loads(response.text)
        for goods_number, item in enumerate(url_detail['items']):
            itemid = item['itemid']
            shopid = item['shopid']
            price_min = item['price_min'] / 100000
            price_max = item['price_max'] / 100000
            image_id = item['image']
            title = item['name']
            historical_sold = item["historical_sold"]
            # 店铺名称、加入时间、保存图片
            # detail_url_title = re.sub('[%/\*\?<>《》\|💥"“]','',title)
            detail_url_title = ''.join(re.findall("[\w ]", title))
            # print(detail_url_title)
            image_url = "https://cf.shopee.com.my/file/{}".format(image_id)
            detail_url = "https://my.xiapibuy.com/{}".format(detail_url_title) + "-i." + str(shopid) + "." + str(itemid)
            detail_url_user = "https://my.xiapibuy.com/api/v2/shop/get?is_brief=1&shopid={}".format(str(shopid))

            yield scrapy.Request(url=detail_url_user,callback=self.parse_user_detail,dont_filter=True,meta={"info":(title,price_min,price_max,historical_sold,detail_url,image_url)})



    def parse_user_detail(self,response):
        title, price_min, price_max, historical_sold, detail_url, image_url = response.meta.get("info")
        response_detail_text = json.loads(response.text)
        username = response_detail_text["data"]["account"]["username"]
        # 加入时间（秒）,转换成天
        ctime = response_detail_text["data"]["ctime"]
        ctime = (int(time.time()) - ctime) / 24 / 3600

        item = ShopeeClothingItem(title=title,price_min=price_min,price_max=price_max,historical_sold=historical_sold,username=username,ctime=ctime,detail_url=detail_url,image_url=image_url)
        yield item


