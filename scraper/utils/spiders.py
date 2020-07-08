"""
This module contains all the scrapy spiders for the scraper module
"""
import scrapy
from .constants import OLXConfig as OLX, ColombiaGamerConfig as CGamer, GamePlanetConfig as GamePl
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


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
        'FEED_EXPORT_ENCODING': 'utf-8',
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
        Retrieves information for all products in terms of the fields: name,
        description, price, image, and url
        """
        product_xp = f'//li[@data-aut-id="{OLX.ITEM_CLASS.value}"]//a/@href'
        product_urls = response.xpath(product_xp).getall()

        for url in product_urls:
            yield response.follow(url, callback = self.parse_product)


class ColombiaGamerSpider(scrapy.Spider):
    """
    This spider scraps products from the ColombiaGamer e-commerce site
    """
    name = CGamer.SPIDER_NAME.value
    custom_settings = {
        'FEEDS': {
            CGamer.EXPORT_FILE_PATH.value: {
                'format': 'json',
                'encoding': 'utf-8',
                'fields': ['name', 'description', 'price', 'image', 'url'],
                'indent': 4
            }
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEPTH_LIMIT': 1,
        'AUTOTHROTTLE_ENABLED': True
    }


    def parse_product(self, response):
        """
        Retrieves product information from the product detail page, and exports
        it to the output json
        """
        self.log(f'\n>>>>> ATTEMPTING TO SCRAP {response.url}<<<<<\n')

        name_xp = f'//div[@class="{CGamer.TITLE_CLASS.value}"]//h2/text()'
        name = response.xpath(name_xp).get()

        desc_xp = f'//div[@class="{CGamer.DESC_CLASS.value}"]/*'
        description_elements = response.xpath(desc_xp).extract()
        description = ''.join(description_elements)

        price_xp = f'//span[@class="{CGamer.PRICE_CLASS.value}"]/text()'
        price = response.xpath(price_xp).get()

        image_xp = (f'//div[@class="{CGamer.IMG_CLASS.value}"]//img/@src')
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
        Retrieves information for all products in terms of the fields: name,
        description, price, image, and url
        """
        product_xp = (f'//div[contains(@class, "{CGamer.ITEM_CLASS.value}")]//'
                      'h2/a/@href')
        product_urls = response.xpath(product_xp).getall()

        for url in product_urls:
            yield response.follow(url, callback = self.parse_product)

class GamePlSpider(scrapy.Spider):
    """
    This spider scraps products from the GamePlanet e-commerce site
    """
    name = GamePl.SPIDER_NAME.value
    custom_settings = {
        'FEEDS': {
            GamePl.EXPORT_FILE_PATH.value: {
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

        self.driver.get(response.url)

        name_xp = f'//h1[@class="{GamePl.TITLE_CLASS.value}"]'
        name = self.driver.find_elements_by_xpath(name_xp)[0].get_attribute('innerText')
        
        self.log('getting_name')
        self.log(name)

        desc_xp = f'//div[@class="{GamePl.DESC_CLASS.value}"]'
        description = self.driver.find_elements_by_xpath(desc_xp)[0].get_attribute('innerText')

        price_xp = f'//div[contains(@class, {GamePl.PRICE_CLASS.value})]//span'
        price = self.driver.find_elements_by_xpath(price_xp)[0].get_attribute('innerText')

        image_xp = (f'//img[@id = "{GamePl.IMAGE_ID.value}"]')
        image_url = self.driver.find_elements_by_xpath(image_xp)[0].get_attribute('src')
        image = image_url

        yield {
            'name': name,
            'description': description,
            'price': price,
            'image': image,
            'url': response.url
        }


    def parse(self, response):
        """
        Retrieves information for all products in terms of the fields: name,
        description, price, image, and url
        """
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(response.url)
        product_xp = (f'//div[contains(@class, "{GamePl.ITEM_CLASS.value}")]/div[@class = "row"]/div/a')
        
        product_urls = self.driver.find_elements_by_xpath(product_xp)
        self.log(product_urls)
        for url in product_urls:
            self.log(url.get_attribute('href'))
            yield response.follow(url.get_attribute('href'), callback = self.parse_product)