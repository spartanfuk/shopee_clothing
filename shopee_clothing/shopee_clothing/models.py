from FreeProxy import ProxyTool

class ProxyModel(object):
    def __init__(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
        }
        pt = ProxyTool.ProxyTool(headers=headers, proxy_type='http')  # , host="http://httpbin.org/ip"
        proxy = pt.getProxy(num_proxies=1, max_tries=10)[0]
        self.proxy = 'http://' + proxy[0] + ':' + proxy[1]

    @property
    def is_expiring(self):
        return ''
