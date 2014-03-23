from scrapy.spider import Spider
from scrapy.selector import Selector

from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from scrapy.http import Request 

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scraper.items import StateItem, DistrictItem, BlockItem, PanchayatItem, Dummy
from scraper.scraperConfig import *
#from django.db import Models
from nregaApp.models import Block, Panchayat
import re

class block_data_spider(Spider):
	name = "block_data"
	blocks = Block.objects.all()
	block_links = [b.link for b in blocks]
	start_urls = [block_links[1]]
	print [x for x in blockDataConfig]
	#rules = ((Rule(SgmlLinkExtractor (restrict_xpaths = link_xpath,) ,callback="parse_block_data", ) for link_xpath in table_link_extractors))

	def parse(self, response):
		sel = Selector(response)
		base_url = get_base_url(response)
		query_dict = parse_url(base_url)

		for table_name in blockDataConfig:
			next_link = urljoin_rfc(base_url, sel.xpath('//a//text()[contains(.,"'+table_name+'")]/ancestor::a/@href').extract()[0])
			request = Request(next_link, self.parse_block_data)
			request.meta['linkText'] = table_name
			request.meta['blockKey'] = Block.objects.get(code__exact=query_dict[block_code]) 
			yield request

	def parse_block_data(self, response):
		sel = Selector(response)
		linkText = response.meta['linkText']
		blockKey = response.meta['blockKey']
		colMapping = blockDataConfig[linkText]
		nameCol = colMapping['name']
		
		#assumes Panchayat objects have been created with name filled in
		panchayats = Panchayat.objects.filter(block = blockKey)
		for panchayat in panchayats:
			for attribute in colMapping:
				if attribute == 'name':
					continue
				print '//tr//td['+str(nameCol)+']//text()[contains(.,"'+panchayat.name[3:-2]+'")]/ancestor::tr/td['+str(colMapping[attribute])+']/text()'
				extractor_path = '//tr//td['+str(nameCol)+']//text()[contains(.,"'+panchayat.name[3:-2]+'")]/ancestor::tr/td['+str(colMapping[attribute])+']/text()'
				nums = re.findall('^[0-9]+',sel.xpath(extractor_path).extract()[0])[0]
				setattr(panchayat, attribute, nums)
			panchayat.save()
		return Dummy()
