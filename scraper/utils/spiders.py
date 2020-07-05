"""
This module contains all the scrapy spiders for the scraper module
"""
import re
import scrapy
from .constants import OLXConfig as OLX, ExitoConfig as Exito

class OLXSpider(scrapy.Spider):
    """
    This spider scraps products from the OLX e-commerce site
    """
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

        price_xp = (f'//section[@class="{OLX.RIGHT_SECT_CLASS.value}"]//span/'
                    'text()')
        price = response.xpath(price_xp).get()

        image_xp = (f'//div[contains(@class, "{OLX.IMG_DIV_CLASS.value}")]//'
                    'img/@src')
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
        product_urls = response.xpath('//li[@data-aut-id="itemBox"]//a/@href')\
                           .getall()

        for url in product_urls:
            yield response.follow(url, callback = self.parse_product)


class ExitoSpider(scrapy.Spider):
    """
    This spider scraps products from the Exito e-commerce site
    """
    name = Exito.SPIDER_NAME.value
    custom_settings = {
        'FEEDS': {
            Exito.EXPORT_FILE_PATH.value: {
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

        name_xp = (f'//span[contains(@class, "{Exito.NAME_CLASS.value}")]/'
                   'text()')
        raw_name = response.xpath(name_xp).get()

        #pattern = re.compile(r'^(?P<name>\"([^\"].)+\")')

        #name = pattern.match(raw_name).group('name').replace('"', '')

        name = raw_name.partition('\r')[0].replace('"', '')

        # desc_xp = (f'//section[@class="{Exito.LEFT_SECT_CLASS.value}"]//p/'
        #            'text()')
        # description = response.xpath(desc_xp).get()

        # price_xp = (f'//section[@class="{Exito.RIGHT_SECT_CLASS.value}"]//span/'
        #             'text()')
        # price = response.xpath(price_xp).get()

        # image_xp = (f'//div[contains(@class, "{Exito.IMG_DIV_CLASS.value}")]//img/@src')
        # image = response.urljoin(response.xpath(image_xp).get())

        yield {
            'name': name#,
            # 'description': description,
            # 'price': price,
            # 'image': image,
            # 'url': response.url
        }


    def parse(self, response):
        """
        Retrieves information for all products: name, description, price, image,
        and url

        Product containers class: itembox
        href of li in all containers is a relative path
        """
        sect_xp = (f'//section[contains(@class, "{Exito.ITEM_CLASS.value}")]//'
                   'a/@href')
        product_urls = response.xpath(sect_xp).getall()

        for url in product_urls:
            yield response.follow(url, callback = self.parse_product)