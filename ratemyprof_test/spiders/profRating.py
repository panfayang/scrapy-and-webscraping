from scrapy.item import Field, Item
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request

class ProfRatingItem(Item):
	name = Field()
	Review = Field()
	Date =  Field()
	Class = Field()
	Quality = Field()
	Easiness = Field()
	Helpfulness = Field()
	Clarity = Field()
	RaterInterest = Field()
	# url = Field()
	curpage = Field()
	school_Name = Field()
	department = Field()
	# overall_Quality = Field()
	# overall_Helpfulness = Field()
	# overall_Clarity = Field()
	# overall_Easiness = Field()
	# overall_Hotness = Field()
	# Number_of_ratings = Field()

class ProfSummaryItem(Item):
	Name = Field()
	# url = Field()
	School_Name = Field()
	Department = Field()
	Overall_Quality = Field()
	Overall_Easiness = Field()
	Hotness = Field()
	Number_of_ratings = Field()

class MySpider(BaseSpider):

	name = 'profRating'
	allow_domains = ['ratemyprofessors.com']
	start_urls = []
	start_urls.append('http://www.ratemyprofessors.com/SelectTeacher.jsp?sid=474')

	def parse(self,response):
		hxs = HtmlXPathSelector(response)
		site = hxs.select('//div[contains(@class,"vertical-center")]')
		for sites in site:
			item1 = ProfSummaryItem()
			# item1['url'] = response.url
			item1['Name'] = sites.select('div[4]/a/text()').extract()
			item1['School_Name'] = hxs.select('//div[@id="profContent"]/div/h2/text()').extract()
			item1['Department'] = sites.select('div[5]/text()').extract()
			item1['Number_of_ratings'] = sites.select('div[6]/text()').extract()
			item1['Overall_Quality'] = sites.select('div[7]/text()').extract()
			item1['Overall_Easiness'] = sites.select('div[8]/text()').extract()
			item1['Hotness'] = sites.select('div[9]/text()').extract()
			yield item1
			if "0" not in str(sites.select('div[6]/text()').extract()[0]):
				reviewUrl = "http://www.ratemyprofessors.com/%s&pageNo=1" %sites.select("div[4]/a/@href").extract()[0]
				yield Request(url=reviewUrl,callback=self.parse_reviews)

		if hxs.select('//a[@id="next"]/text()').extract():
			url =   "http://www.ratemyprofessors.com%s"%hxs.select('//a[@id="next"]/@href').extract()[0]
			yield Request(url=url,callback=self.parse)

	def parse_reviews(self,response):
		hxs = HtmlXPathSelector(response)
		site = hxs.select('//div[@class="entry odd " or @class="entry even "]')
		info = hxs.select('//div[@id="profInfo"]')
		# scoreCard = hxs.select('//div[@id="scoreCard"]')
		for sites in site:
			item = ProfRatingItem()
			# item['url'] = response.url
			item['Review'] = sites.select('div[4]/p/text()').extract()
			item['Date'] = sites.select('div[1]/text()').extract()[0]
			item['Class'] = sites.select('div[2]/p/text()').extract()
			item['Quality']= sites.select('div[3]/p/text()').extract()
			item['Easiness'] = sites.select('div[3]/p[2]/span/text()').extract()
			item['Helpfulness'] = sites.select('div[3]/p[3]/span/text()').extract()
			item['Clarity'] = sites.select('div[3]/p[4]/span/text()').extract()
			item['RaterInterest'] = sites.select('div[3]/p[5]/span/text()').extract()
			item["name"] = hxs.select('//h2[@id="profName"]/text()').extract()
			item["curpage"] = response.url[-1]
			item['school_Name'] = info.select('ul/li[1]/strong/a/text()').extract()
			item["department"] = info.select('ul/li[3]/strong/a/text()').extract()
			# item["overall_Quality"] = scoreCard.select('ul/li[1]/a/strong/text()').extract()
			# item["overall_Helpfulness"] = scoreCard.select('ul/li[2]/a/strong/text()').extract()
			# item["overall_Clarity"] = scoreCard.select('ul/li[3]/a/strong/text()').extract()
			# item["overall_Easiness"] = scoreCard.select('ul/li[4]/a/strong/text()').extract()
			# item["overall_Hotness"] = hxs.select('//li[contains(@title,"Hot professors")]/a/strong/text()').extract()
			# item["Number_of_ratings"] = hxs.select('//span[@id="rateNumber"]/strong/text()').extract()
			yield item
		if hxs.select('//a[@id="next"]/text()').extract():
			url =   "http://www.ratemyprofessors.com%s"%hxs.select('//a[@id="next"]/@href').extract()[0]
			yield Request(url=url,callback=self.parse)
