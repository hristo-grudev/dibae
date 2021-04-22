import json

import scrapy

from scrapy.loader import ItemLoader

from ..items import DibaeItem
from itemloaders.processors import TakeFirst


class DibaeSpider(scrapy.Spider):
	name = 'dibae'
	start_urls = ['https://www.dib.ae/about-us/media-center/news/GetMediaCenterNews/?type=news']

	def parse(self, response):
		data = json.loads(response.text)
		for post in data['MergedMediaCenterList']:
			url = post['UrlName']
			date = post['FormattedDate']
			title = post['Title']
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, title, date):
		description = response.xpath('//div[@class="media-information"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=DibaeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
