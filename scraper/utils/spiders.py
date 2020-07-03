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
        'DEPTH_LIMIT': 1,
        'AUTOTHROTTLE_ENABLED': True
    }


    def parse_product(self, response):
        """
        Retrieves product information from the product detail page, and exports
        it to the output json
        """
        self.log('0000000000000000000000000000000000000000000000')

        name_xp = f'//section[@class="{OLX.RIGHT_SECT_CLASS.value}"]/h1/text()'
        name = response.xpath(name_xp).get()

        yield {
            'name': name#,
            # 'description': 'here description',
            # 'price': '"$$$',
            # 'image': 'url to image',
            # 'url': f'url to offer post'
        }


    def parse(self, response):
        """
        Retrieves information for all products: name, description, price, image, url

        Product containers class: itembox
        href of li in all containers is a relative path
        """
        product_urls = response.xpath('//li[@data-aut-id="itemBox"]//a/@href').getall()

        for url in product_urls:
            # yield {
            #     'name': url#,
            #     # 'description': 'here description',
            #     # 'price': '"$$$',
            #     # 'image': 'url to image',
            #     # 'url': f'url to offer post'
            # }
            self.log(f'!!!!!!!!! TRYING TO FOLLOW {url} -- {response.url}')
            yield response.follow(url, callback = self.parse_product)