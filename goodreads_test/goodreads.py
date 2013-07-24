from scrapy.item import Item,Field
from scrapy.spider import BaseSpider
# from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re
from scrapy import log
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.contrib.loader import XPathItemLoader

from scrapy.contrib.loader.processor import TakeFirst

class GoodreadsTestItem(Item):
  title = Field()
	pass

class MySpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)
        self.counter = 1

    name = 'goodreads'
    allow_domains = ['goodreads.com']
    start_urls = ['http://www.goodreads.com/book/show/221304?page=1&amp;sort=oldest']
    def parse(self, response):
    # response = response.replace(body=response.body.replace("disabled",""))
        xs = HtmlXPathSelector(response)
        requests = []
        print "@@@@@@@@@@@@@@@@@@"+response.url
        requests.append(Request(response.url,callback=self.parse_item))
        self.parse_item(response)
        if xs.select('//a[@class="next_page"]/@class').extract():
            print "***************************************************************"
            print self.counter
            requests.append(FormRequest.from_response(
                    response,
                    formxpath='//a[@class="next_page"]',
                    callback=self.parse
                )
            )
        print requests
        for request in requests:
            yield request
        
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        print "-----------------------------------------------------------------------"
        print response.url
        # sites = hxs.select('//div[contains(@id,"BVRRDisplayContentReviewID")]')
        # sites = hxs.select('//div[@id="BVSubmissionPopupContainer"]')
        sites = hxs.select('//a[@class="user"]')
        items = []
        for site in sites:
            item = GoodreadsTestItem()
            # item['title'] = sites.select('div[2]/div/div/span[2]/text()').extract()
            item['title'] = site.select('@title').extract()
            items.append(item)
        return items



    # def parse(self, response):
    # # response = response.replace(body=response.body.replace("disabled",""))
    #     xs = HtmlXPathSelector(response)
    #     requests = []
    #     print "@@@@@@@@@@@@@@@@@@"+response.url
    #     requests.append(Request(response.url,callback=self.parse_item))
    #     # self.parse_item(response)
    #     if xs.select('//a[@class="next_page"]/@class').extract():
    #         print "***************************************************************"
    #         print self.counter
    #         self.counter += 1
    #         url = 'http://www.goodreads.com/book/show/221304?page=%s&amp;sort=oldest' %self.counter
    #         requests.append(Request(url=url,callback=self.parse))
    #     print requests
    #     for request in requests:
    #         yield request
        
    # def parse_item(self, response):
    #     hxs = HtmlXPathSelector(response)
    #     print "-----------------------------------------------------------------------"
    #     print response.url
    #     # sites = hxs.select('//div[contains(@id,"BVRRDisplayContentReviewID")]')
    #     # sites = hxs.select('//div[@id="BVSubmissionPopupContainer"]')
    #     sites = hxs.select('//a[@class="user"]')
    #     items = []
    #     for site in sites:
    #         item = GoodreadsTestItem()
    #         # item['title'] = sites.select('div[2]/div/div/span[2]/text()').extract()
    #         item['title'] = site.select('@title').extract()
    #         items.append(item)
    #     return items
