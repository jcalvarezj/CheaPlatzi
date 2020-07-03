"""
This module contains all the scrapy spiders for the scraper module
"""
from .constants import OLXConfig as OLX
import scrapy

class OLXSpider(scrapy.Spider):
    name = OLX.SPIDER_NAME.value
    custom_settings = {
        'FEEDS': {
            OLX.EXPORT_FILE_PATH.value: {
                'format': 'json',
                'encoding': 'utf-8',
                'fields': ['name', 'description', 'price', 'image', 'url'],
                'indent': 4
            }
        },
        "FEED_EXPORT_ENCODING": "utf-8",
        'DEPTH_LIMIT': 1,
        'AUTOTHROTTLE_ENABLED': True
    }


    def parse_product(self, response):
        """
        Retrieves product information from the product detail page, and exports
        it to the output json
        """
        self.log(f'>>>>> ATTEMPTING TO SCRAP {response.url}<<<<<')

        name_xp = f'//section[@class="{OLX.RIGHT_SECT_CLASS.value}"]/h1/text()'
        name = response.xpath(name_xp).get()

        desc_xp = f'//section[@class="{OLX.LEFT_SECT_CLASS.value}"]//p/text()'
        description = response.xpath(desc_xp).get()

        price_xp = f'//section[@class="{OLX.RIGHT_SECT_CLASS.value}"]//span/text()'
        price = response.xpath(price_xp).get()

        image_xp = f'//div[contains(@class, "{OLX.IMG_DIV_CLASS.value}")]//img/@src'
        image = response.urljoin(response.xpath(image_xp).get())

        yield {
            'name': name,
            'description': description,
            'price': price,
            'image': image,
            'url': response.url
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
            full_url = response.urljoin(url)
            # self.log(f'\n!!!!!!!!! TRYING TO FOLLOW {new_url}\n')
            yield response.follow(url, callback = self.parse_product)