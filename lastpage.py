"""
This module finds the last page of an amazon product review from the first page.
Fayang Pan
7/3/13

Modified as of 7/16/13
Now it processes multiple ASINs at the same time.

"""

__author__ = "Fayang Pan"
__version__ = "$Revision: 2.3$"
__date__ = "$7/18/2013$"
__copyright__ = "Copyright (c) 2013 Fayang Pan"
__license__ = "Python, Scrapy"

from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from grabItems import GrabItems
from scrapy import log

class LastItem(Item):
    ID = Field()
    lastPage = Field()

class MySpider2(BaseSpider):
   
    grab = GrabItems()
    validIDLoc = "%sValidifiedIDs.txt" %grab.scrapy_dir
    IDs = grab.grabID(validIDLoc)
    name = "grablastpage"
    allow_domains = ["amazon.com"]
    
    ## The first pages.
    start_urls = []
    for ASIN in IDs:
        start_urls.append('http://www.amazon.com/gp/product-reviews/%s/?ie=UTF8&sortBy=bySubmissionDateAscending&showViewpoints=0&pageNumber=0.html' %ASIN)

    def parse(self, response):
        """
        Checks the last page from the first page
        """
        hxs = HtmlXPathSelector(response)
        item = LastItem()
        item["ID"] = response.url.split("/")[5]
        try:
            lpnum = hxs.select('//div[@class="CMpaginate"]/span/a[2]/text()').extract()[0]
        except IndexError:
            item['lastPage'] = 1
        else:
            item['lastPage'] = lpnum
            if 'ext' in lpnum:
                item['lastPage'] = 2

        try:
            maybe4 = hxs.select('//div[@class="CMpaginate"]/span/a[3]/text()').extract()[0]
        except IndexError:
            pass
        else:
            if '4' in maybe4:
                item["lastPage"] = 4
        return item
