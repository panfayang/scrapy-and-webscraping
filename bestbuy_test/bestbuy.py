##UNFINISHED
from scrapy.item import Item,Field
from scrapy.spider import BaseSpider
# from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re
from scrapy import log

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider


class BestbuyTestItem(Item):
  title = Field()
	pass

class MySpider(BaseSpider):
    name = 'bestbuy'
    allow_domains = ['bestbuy.com']
    start_urls = ['http://www.bestbuy.com/site/%20/.p?id=1218321299000']

    def parse(self, response):
    # response = response.replace(body=response.body.replace("disabled",""))
        xs = HtmlXPathSelector(response)
        requests = []
        self.parse_item(response)
        if xs.select('//a[@title="next"]/text()').extract():
            requests.append(FormRequest.from_response(response,
                    formname={'BV_TrackingTag_Review_Display_NextPage':True},
                    callback=self.parse))
                
        for request in requests:
            yield request
        
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        # sites = hxs.select('//div[contains(@id,"BVRRDisplayContentReviewID")]')
        # sites = hxs.select('//div[@id="BVSubmissionPopupContainer"]')
        sites = hxs.select('//div[@itemprop="reviews"]')
        items = []
        for site in sites:
            item = BestbuyTestItem()
            # item['title'] = sites.select('div[2]/div/div/span[2]/text()').extract()
            item['title'] = site.select('span[1]/text()').extract()
            items.append(item)
        return items
