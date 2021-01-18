# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from FreeProxy import ProxyTool
from shopee_clothing.models import ProxyModel
from twisted.internet.defer import DeferredLock
import json
from twisted.internet.error import TimeoutError,TCPTimedOutError
import time

class UserAgentDownloadMiddleware(object):
    ua = UserAgent()
    user_agent = ua.chrome
    headers = None

    def process_request(self,request,spider):
        # for keys,value in self.headers.items():
        #     request.headers[keys] = value
        # request.headers['User-Agent'] = self.user_agent

        request.headers['User-Agent'] = self.user_agent
        # print(request.headers)

class IPProxyDownloadMiddleware(object):

    def __init__(self):
        super(IPProxyDownloadMiddleware,self).__init__()
        self.current_proxy = None
        self.lock = DeferredLock()
        self.blacked = False
        self.get_proxy = False
        self.proxies = []
        # self.proxies_time = 9999999999
        self.proxies_time = time.time()

    def process_request(self,request,spider):
        # print(request.headers)
        # if not self.get_proxy:
        if ('proxy' not in request.meta) :# & (self.get_proxy):#
            self.update_proxy()
        request.meta['proxy'] = self.current_proxy
        # self.proxies_time = time.time()

        print("process_request:", request.meta['proxy'])
        # else:
        #     print('使用本机ip！')

    def process_response(self,request,response,spider):
        url_detail = json.loads(response.text)
        # print('=' * 30)
        # print("request_response")
        # print('=' * 30)
        if "sales" in response.url:
            print('=' * 30)
            print("request_sales")
            print('=' * 30)
            if url_detail.get("items") == None:
                # if not self.get_proxy:
                #     self.get_proxy = True
                print('=' * 50)
                print("爬取image_id为空！，获取代理ip")
                print(url_detail.get("items"))
                if not self.blacked:
                    self.blacked = True
                    self.proxies.append(self.current_proxy)
                print(response.url)
                print("%s这个代理被加入黑名单" % self.current_proxy)
                print(self.proxies)
                print('=' * 50)
                self.update_proxy()
                return request
            elif len(str(url_detail.get("items")[0].get("image"))) != 32:
                print('=' * 50)
                print("爬取image_id != 32位！，获取代理ip")
                # if not self.get_proxy:
                #     self.get_proxy = True
                if not self.blacked:
                    self.blacked = True
                    self.proxies.append(self.current_proxy)
                print(response.url)
                print("%s这个代理被加入黑名单" % self.current_proxy)
                print(self.proxies)
                print('=' * 50)
                self.update_proxy()
                return request
        # elif "sales" not in response.url:
        else:
            # print('=' * 30)
            # print("request_detail")
            # print('=' * 30)
            if response.status != 200:
                print('=' * 50)
                print("爬取username有误！，获取代理ip")
                # if not self.get_proxy:
                #     self.get_proxy = True
                if not self.blacked:
                    self.blacked = True
                    self.proxies.append(self.current_proxy)
                print(response.url)
                print("%s这个代理被加入黑名单" % self.current_proxy)
                print(self.proxies)
                print('=' * 50)
                self.update_proxy()
                return request
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            print('=' * 50)
            print("爬取username出现TimeoutError！，获取代理ip")
            # if not self.get_proxy:
            #     self.get_proxy = True
            if not self.blacked:
                self.blacked = True
                self.proxies.append(self.current_proxy)
            print("%s这个代理被加入黑名单" % self.current_proxy)
            print(self.proxies)
            print('=' * 50)
            self.update_proxy()
            return request
        elif isinstance(exception,TCPTimedOutError):
            print('=' * 50)
            print("爬取username出现TCPTimedOutError！，获取代理ip")
            # if not self.get_proxy:
            #     self.get_proxy = True
            if not self.blacked:
                self.blacked = True
                self.proxies.append(self.current_proxy)
            print("%s这个代理被加入黑名单" % self.current_proxy)
            print(self.proxies)
            print('=' * 50)
            self.update_proxy()
            return request

    # def spider_opened(self, spider):
    #     spider.logger.info('Spider opened: %s' % spider.name)

    def update_proxy(self):
        self.lock.acquire()
        if (time.time() - self.proxies_time) >= 600:
            self.proxies = []
        if not self.current_proxy or self.blacked:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
            }
            print("update_proxy")
            pt = ProxyTool.ProxyTool(headers=headers, proxy_type='https',host="https://my.xiapibuy.com/")  # ,host="https://my.xiapibuy.com/"
            while True:
                proxy_str = pt.getProxy(num_proxies=1, max_tries=20)
                # print(proxy_str)
                # if (proxy_str != []) & (proxy_str not in self.proxies):
                #     proxy = 'https://' + proxy_str[0][0] + ':' + proxy_str[0][1]
                #     self.current_proxy = proxy
                #     self.blacked = False
                #     break

                if proxy_str == []:
                    continue
                else:
                    proxy = 'https://' + proxy_str[0][0] + ':' + proxy_str[0][1]
                    if proxy not in self.proxies:
                        self.current_proxy = proxy
                        self.blacked = False
                        break

            print("重新获取了一个代理", proxy_str)
        self.lock.release()

