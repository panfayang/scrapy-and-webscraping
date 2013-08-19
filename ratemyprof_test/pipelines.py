

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from ratemyprof_test.spiders.profRating import ProfRatingItem,ProfSummaryItem

class MultiCSVItemPipeline(object):
    def __init__(self):
        self.files = {}
        self.exporter1 = CsvItemExporter(fields_to_export=ProfRatingItem.fields.keys(),file=open("profRating.csv",'wb'))
        self.exporter2 = CsvItemExporter(fields_to_export=ProfSummaryItem.fields.keys(),file=open("profSummary.csv",'wb'))

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

    def spider_opened(self, spider):
    	self.exporter1.start_exporting()
    	self.exporter2.start_exporting()

    def spider_closed(self, spider):
        self.exporter1.finish_exporting()
        self.exporter2.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter1.export_item(item)
        self.exporter2.export_item(item)
        return item
