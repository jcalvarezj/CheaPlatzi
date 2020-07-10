"""
This module contains all the scrapy spiders for the scraper module
"""
import time
import scrapy
from .constants import SITE_IDS
from .constants import OLXConfig as OLX, ColombiaGamerConfig as CGamer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
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
                'fields': ['id_type_product', 'id_ecommerce', 'name',
                           'description', 'price', 'image', 'url'],
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
        price = int(response.xpath(price_xp).get().replace('$ ','') \
                    .replace('.', ''))

        image_xp = (f'//div[contains(@class, "{OLX.IMG_DIV_CLASS.value}")]//'
                    'img/@src')
        image = response.urljoin(response.xpath(image_xp).get())

        yield {
            'id_type_product': None,
            'id_ecommerce': SITE_IDS['OLX'],
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

        button_xp = f'//button[@data-aut-id="{OLX.BTN_CLASS.value}"]'

        try:
            WebDriverWait(self.driver, OLX.DRIVER_TIMEOUT.value).until(
                EC.presence_of_element_located((By.XPATH, button_xp))
            )
        except TimeoutError:
            self.log('The page took too long to load. Reached timeout.')
        
        button = self.driver.find_element_by_xpath(button_xp)

        while button:
            try:
                button.click()
                time.sleep(OLX.DELAY_IN_SECS.value)
            except StaleElementReferenceException:
                button = None

        product_xp = f'//li[@data-aut-id="{OLX.ITEM_CLASS.value}"]/a[@href]'
        a_tags = self.driver.find_elements_by_xpath(product_xp)
        product_urls = [a.get_attribute('href') for a in a_tags]

        self.driver.close()

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
                'fields': ['id_type_product', 'id_ecommerce', 'name',
                           'description', 'price', 'image', 'url'],
                'indent': 4
            }
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
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

        short_desc_xp = f'//div[@class="{CGamer.SHORT_DESC_CLASS.value}"]/*'
        short_desc_elements = response.xpath(short_desc_xp).extract()
        short_description = ''.join(short_desc_elements)

        desc_xp = f'//div[@class="{CGamer.DESC_CLASS.value}"]/*'
        description_elements = response.xpath(desc_xp).extract()
        big_description = ''.join(description_elements)
        description = f'{short_description}\n{big_description}'

        price_xp = f'//span[@class="{CGamer.PRICE_CLASS.value}"]/text()'
        price = int(response.xpath(price_xp).get().replace('$ ','') \
                    .replace('.', ''))

        image_xp = (f'//div[@class="{CGamer.IMG_CLASS.value}"]//img/@src')
        image = response.urljoin(response.xpath(image_xp).get())

        yield {
            'id_type_product': None,
            'id_ecommerce': SITE_IDS['ColombiaGamer'],
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

        list_items = response.xpath('//nav[@role="pagination"]//li/@class')
        page_buttons_xp = '//nav[@role="pagination"]//a/@href'
        page_buttons = response.xpath(page_buttons_xp).getall()

        if len(page_buttons) > 1:
            last_item_class = list_items[-1]
            if last_item_class != 'active':
                next_page = page_buttons[-2]
                yield response.follow(next_page, callback = self.parse)

        product_xp = (f'//div[contains(@class, "{CGamer.ITEM_CLASS.value}")]//'
                      'h2/a/@href')
        product_urls = response.xpath(product_xp).getall()

        for url in product_urls:
            yield response.follow(url, callback = self.parse_product)