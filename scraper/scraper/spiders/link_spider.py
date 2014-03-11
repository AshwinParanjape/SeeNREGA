from scrapy.spider import Spider
from scrapy.selector import Selector

from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from scrapy.http import Request 

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scraper.items import StateItem, DistrictItem, BlockItem, PanchayatItem, Dummy
from scraper.scraperConfig import *
class link_spider(CrawlSpider):
	name = "links"
	start_urls = [ "http://nrega.nic.in/Netnrega/stHome.aspx" ]
	rules = (
			#Extract links for each state
			Rule(SgmlLinkExtractor ( allow = '.*homestciti.*',), follow=True, callback="open_english",),
			#Rule(SgmlLinkExtractor ( restrict_xpaths = district_extractor,), callback="parse_block_list"),
			#Rule(SgmlLinkExtractor ( restrict_xpaths = block_extractor,), callback = "parse_village_list", ),
			)
	
	def parse_block_list(self,response):
		sel = Selector(response);
		base_url = get_base_url(response)
		anchorList = sel.xpath(block_extractor)
		itemList = []
		for anchor in anchorList:
			item = block()
			item['name'] = anchor.xpath('./text()').extract();
			item['link'] = urljoin_rfc(base_url, anchor.xpath('./@href').extract()[0])
			itemList.append(item)
		return itemList

		return []
	def open_english(self, response):
		sel = Selector(response);
		base_url = get_base_url(response)
		base_url = base_url+'&lflag=eng'
		request = Request(base_url, self.parse_district_list)
		return request


	def parse_district_list(self,response):
		sel = Selector(response);
		base_url = get_base_url(response)
		query_dict = parse_url(base_url)

		state = StateItem()
		state ['name'] = query_dict[state_name]
		state ['code' ] = query_dict[state_code]
		stateInstance = state.save()

		anchorList = sel.xpath(district_extractor)
		itemList = []
		for anchor in anchorList:
			item = DistrictItem()
			item['state'] = stateInstance
			item['name'] = anchor.xpath('./text()').extract()
			query_dict = parse_url(anchor.xpath('./@href').extract()[0])
			item['code'] = query_dict[district_code]
			item.save()

		return Dummy()
