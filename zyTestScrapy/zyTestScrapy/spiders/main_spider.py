import re
import json

from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
# from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor as sle

from scrapy.http import Request


from zyTestScrapy.items import *
from zyTestScrapy.misc.log import *


class TencentSpider(CrawlSpider):
    name = "Hu_Nan_University"
    allowed_domains = ["hnu.edu.cn"]
    start_urls = [
        #"http://hr.tencent.com/position.php"
        # "http://scc.hnu.edu.cn"
        "http://scc.hnu.edu.cn/newsjob.action"
    ]
    rules = [
        #http://scc.hnu.edu.cn/newsjob!getMore.action?Lb=1&p.currentPage=1
        #http://scc.hnu.edu.cn/newsjob!getMore.action?p.currentPage=1&Lb=1
        #http://scc.hnu.edu.cn/newsjob!getMore.action?p.currentPage=2&Lb=1
        #http://scc.hnu.edu.cn/newsjob!getMore.action?p.currentPage=3&Lb=1
        Rule(sle(allow=("/newsjob!getMore.action\?Lb=1&p.currentPage=\d{,4}")), follow=True, callback='parse_item')
        # Rule(sle(allow=("/newsjob!getMore.action\?p.currentPage=\d{,4}&Lb=1")), follow=True, callback='parse_item')
        #http://hr.tencent.com/position.php?&start=10#a
        # Rule(sle(allow=("/position.php\?&start=\d{,4}#a")), follow=True, callback='parse_item')
    ]
    next_page = 1
    spider_url = 'http://scc.hnu.edu.cn/newsjob!getMore.action?Lb=1&p.currentPage='

    def parse_item(self, response):
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)
        # sites_even = sel.css('table.tablelist tr.even')
        sites_list = sel.css('div.r_list1 ul li')
        for site in sites_list:
            item = ZytestscrapyItem()
            # item['name'] = site.css('.l.square a').xpath('text()').extract()[0]
            item['name'] = site.css(' a').xpath('text()').extract()[0]
            relative_url = site.css(' a').xpath('@href').extract()[0]
            item['detailLink'] = urljoin_rfc(base_url, relative_url)
            # item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()[0]
            # item['workLocation'] = site.css('tr > td:nth-child(4)::text').extract()[0]
            # item['recruitNumber'] = site.css('tr > td:nth-child(3)::text').extract()[0]
            item['publishTime'] = site.css(' span').xpath('text()').extract()[0]
            items.append(item)
            #print repr(item).decode("unicode-escape") + '\n'

        # sites_odd = sel.css('table.tablelist tr.odd')
        # for site in sites_odd:
        #     item = ZytestscrapyItem()
        #     item['name'] = site.css('.l.square a').xpath('text()').extract()[0]
        #     relative_url = site.css('.l.square a').xpath('@href').extract()[0]
        #     item['detailLink'] = urljoin_rfc(base_url, relative_url)
        #     item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()[0]
        #     item['workLocation'] = site.css('tr > td:nth-child(4)::text').extract()[0]
        #     item['recruitNumber'] = site.css('tr > td:nth-child(3)::text').extract()[0]
        #     item['publishTime'] = site.css('tr > td:nth-child(5)::text').extract()[0]
        #     items.append(item)
            #print repr(item).decode("unicode-escape") + '\n'

            yield item
        info('parsed ' + str(response))
        
        # return items
        self.next_page = self.next_page + 1
        next_link = self.spider_url + str(self.next_page)
        print "-------------------------------"+next_link
        yield Request(next_link,callback=self.parse_item)


    # def _process_request(self, request):
    #     info('process ' + str(request))
    #     return request

