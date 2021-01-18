# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopeeClothingItem(scrapy.Item):
    # goods_detail = {
    #     'title': title,
    #     'price_min': price_min,
    #     'price_max': price_max,
    #     'historical_sold': historical_sold,
    #     'username': username,
    #     'ctime': ctime,
    #     'detail_url': detail_url,
    #     'image_url': image_url
    # }
    title = scrapy.Field()
    price_min = scrapy.Field()
    price_max = scrapy.Field()
    historical_sold = scrapy.Field()
    username = scrapy.Field()
    ctime = scrapy.Field()
    detail_url = scrapy.Field()
    image_url = scrapy.Field()


