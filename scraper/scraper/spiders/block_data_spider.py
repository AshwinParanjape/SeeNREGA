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
from nregaApp.models import District, Block, Panchayat, PanchayatData
import re
import django
django.setup()
from django.db import transaction

class block_data_spider(Spider):
	name = "block_data"
	
	block = Block.objects.get(code = '219004')
	#blocks = Block.objects.filter(district_id= '0219')
	#block_links = [b.link for b in blocks]
	#start_urls = block_links
	start_urls = [block.link]
	print [x for x in blockDataConfig]
	#rules = ((Rule(SgmlLinkExtractor (restrict_xpaths = link_xpath,) ,callback="parse_block_data", ) for link_xpath in table_link_extractors))

	def parse(self, response):
		sel = Selector(response)
		base_url = get_base_url(response)
		query_dict = parse_url(base_url)
		for key in query_dict:
			query_dict[key.lower()] = query_dict[key]

		for table_name in blockDataConfig:
			next_link = urljoin_rfc(base_url, sel.xpath('//a//text()[contains(.,"'+table_name+'")]/ancestor::a/@href').extract()[0])
			request = Request(next_link, self.parse_block_data)
			request.meta['linkText'] = table_name
			request.meta['query_dict']=query_dict
			request.meta['blockKey'] = Block.objects.get(code=query_dict[block_code]+'') 
			yield request

	def getAttributeVal(self ,l, ind):
		try:
			    b = l[ind]
		except IndexError:
			    b = 0
		return b

	@transaction.atomic
	def parse_block_data(self, response):
		sel = Selector(response)
		linkText = response.meta['linkText']
		blockKey = response.meta['blockKey']
		query_dict = response.meta['query_dict'];
		tableNum = blockDataConfig[linkText][0]
		nameCol = blockDataConfig[linkText][1]
		colMapping = blockDataConfig[linkText][2]
		
		#assumes Panchayat objects have been created with name filled in
		panchayats = Panchayat.objects.filter(block = blockKey)
		#panchayats = [Panchayat.objects.get(code = '219004021')];
		newRows = []
		for panchayat in panchayats:
			panchayat_row_extractor = '//tr//td['+str(nameCol)+']//descendant-or-self::*[text() ="'+panchayat.name+'"]/ancestor::tr'
			row_selector = sel.xpath(panchayat_row_extractor)
			for colNum in colMapping:

				print '//tr//td['+str(nameCol)+']//descendant-or-self::*[text()="'+panchayat.name+'"]/ancestor::tr/td['+str(colNum)+']//text()'
				data_path = 'td['+str(colNum)+']//text()'
				print row_selector.xpath(data_path).extract();
				numString = ''.join(row_selector.xpath(data_path).extract()).strip()
				nums = re.findall('^[0-9]+',numString)[0]

				newRows.append(PanchayatData(state_code = query_dict[state_code],
						district_code = query_dict[district_code],
						block_code = query_dict[block_code],
						panchayat_code = panchayat.code,
						year = query_dict[year][:4],
						attribute_0 = tableNum,
						attribute_1 = self.getAttributeVal(colMapping[colNum],0),
						attribute_2 = self.getAttributeVal(colMapping[colNum],1),
						attribute_3 = self.getAttributeVal(colMapping[colNum],2),
						data = nums))

				#obj, created = PanchayatData.objects.update_or_create(
				#		state_code = query_dict[state_code],
				#		district_code = query_dict[district_code],
				#		block_code = query_dict[block_code],
                #       panchayat_code = panchayat.code,
				#		year = query_dict[year][:4],
				#		attribute_0 = tableNum,
				#		attribute_1 = self.getAttributeVal(colMapping[colNum],0),
				#		attribute_2 = self.getAttributeVal(colMapping[colNum],1),
				#		attribute_3 = self.getAttributeVal(colMapping[colNum],2),
				#		defaults = {'data':nums}
				#		);
			#	panchayat_data.data = nums
			#panchayat.save()
		PanchayatData.objects.bulk_create(newRows);
		return Dummy()
