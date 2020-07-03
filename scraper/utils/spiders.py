"""
This module contains all the scrapy spiders for the scraper module
"""
from .constants import OLXConfig as OLX
import scrapy

class OLXSpider(scrapy.Spider):
    name = OLX.SPIDER_NAME.value
    allowed_domains = [OLX.BASE_DOMAIN.value]
    custom_settings = {
        'FEEDS': {
            OLX.EXPORT_FILE_PATH.value: {
                'format': 'json',
                'encoding': 'utf8',
                'fields': ['name', 'description', 'price', 'image', 'url'],
                'indent': 4            
            }
        },
        'DEPTH_LIMIT': 1
    }


    def parse(self, response):
        """
        Retrieves information for all products: name, description, price, image, url

        Product containers class: itembox
        href of li in all containers is a relative path
        """
        product_names = response.xpath('//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemTitle"]/text()').getall()

        for name in product_names:
            yield {
                'name': name#,
                # 'description': 'here description',
                # 'price': '"$$$',
                # 'image': 'url to image',
                # 'url': f'url to offer post'
            }