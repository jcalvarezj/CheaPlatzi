"""
This module contains all the scrapy spiders for the scraper module
"""
import re
import time
import json
import scrapy
from ..utils.commons import validate_sku
from .constants import GamePlanetConfig as GamePl, MixUpConfig as MU
from .constants import OLXConfig as OLX, ColombiaGamerConfig as CGamer
from .constants import SITE_IDS, BRAND_IDS, SPIDER_EXPORT, SearsConfig as SEA
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException


class OLXSpider(scrapy.Spider):
    """
    This Spider scraps products from the OLX e-commerce site
    """
    name = OLX.SPIDER_NAME.value
    custom_settings = {
        'FEEDS': {
            OLX.EXPORT_FILE_PATH.value: SPIDER_EXPORT
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEPTH_LIMIT': 1,
        'AUTOTHROTTLE_ENABLED': True
    }


    def __init__(self, *args, **kwargs):
        """
        Constructor that initializes the Spider instance and sets it up
        """
        super().__init__(*args, **kwargs)
        chrome_options = Options()  
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                       chrome_options = chrome_options)


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        This method connects the Spider with a termination signal in order to
        automatically execute operations when the Spider closes
        """
        spider = super(OLXSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal = scrapy.signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        """
        Function that is called in the moment of Spider termination. The Spider
        calls it's Selenium driver quit method
        """
        self.driver.close()
        spider.driver.quit()


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

        if not description:
            description = ''

        price_xp = (f'//section[@class="{OLX.RIGHT_SECT_CLASS.value}"]//span/'
                    'text()')
        price = int(response.xpath(price_xp).get().replace('$ ','') \
                    .replace('.', ''))

        image_xp = (f'//div[contains(@class, "{OLX.IMG_DIV_CLASS.value}")]//'
                    'img/@src')
        image = response.urljoin(response.xpath(image_xp).get())

        barcode_xp = f'//div[@class="{OLX.ID_CLASS.value}"]'
        barcode_content = response.xpath(barcode_xp).get()
        barcode = 0

        try:
            barcode = re.search('\d{4,}', barcode_content)[0]
        except:
            print(f'No barcode found for {name}')

        yield {
            'id_type_product': response.meta['brand'],
            'id_ecommerce': SITE_IDS['OLX'],
            'name': name,
            'description': description,
            'price': price,
            'image': image,
            'url': response.url,
            'barcode': int(barcode)
        }


    def parse(self, response):
        """
        Retrieves information for all products in terms of the fields: name,
        description, price, image, and url
        """
        self.driver.get(response.url)

        button_xp = f'//button[@data-aut-id="{OLX.BTN_CLASS.value}"]'
        button = None

        try:
            WebDriverWait(self.driver, OLX.DRIVER_TIMEOUT.value).until(
                EC.presence_of_element_located((By.XPATH, button_xp))
            )
            button = self.driver.find_element_by_xpath(button_xp)
        except TimeoutException:
            self.log('The page took too long to load. Reached timeout.')
            button = False
        
        while button:
            try:
                button.click()
                time.sleep(OLX.DELAY_IN_SECS.value)
            except StaleElementReferenceException:
                button = None

        product_xp = f'//li[@data-aut-id="{OLX.ITEM_CLASS.value}"]/a[@href]'
        a_tags = self.driver.find_elements_by_xpath(product_xp)
        product_urls = [a.get_attribute('href') for a in a_tags]

        brand = None

        if 'ps4' in response.url or 'playstation' in response.url:
            brand = BRAND_IDS['playstation']
        elif 'nintendo' in response.url or 'switch' in response.url:
            brand = BRAND_IDS['nintendo']
        elif 'xbox' in response.url:
            brand = BRAND_IDS['xbox']

        for url in product_urls:
           yield response.follow(url, callback = self.parse_product,
                                 meta = { 'brand': brand })


class ColombiaGamerSpider(scrapy.Spider):
    """
    This Spider scraps products from the ColombiaGamer e-commerce site
    """
    name = CGamer.SPIDER_NAME.value
    custom_settings = {
        'FEEDS': {
            CGamer.EXPORT_FILE_PATH.value: SPIDER_EXPORT
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

        barcode_xp = f'//script[@type="{CGamer.ID_CLASS.value}"]/text()'
        barcode_content = response.xpath(barcode_xp).get()
        barcode = json.loads(barcode_content)['sku']

        yield {
            'id_type_product': response.meta['brand'],
            'id_ecommerce': SITE_IDS['ColombiaGamer'],
            'name': name,
            'description': description,
            'price': price,
            'image': image,
            'url': response.url,
            'barcode': int(barcode)
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

        brand = None

        if 'ps4' in response.url or 'playstation' in response.url:
            brand = BRAND_IDS['playstation']
        elif 'nintendo' in response.url or 'switch' in response.url:
            brand = BRAND_IDS['nintendo']
        elif 'xbox' in response.url:
            brand = BRAND_IDS['xbox']

        for url in product_urls:
            yield response.follow(url, callback = self.parse_product,
                                  meta = { 'brand': brand })


class GamePlSpider(scrapy.Spider):
    """
    This spider scraps products from the GamePlanet e-commerce site
    """
    name = GamePl.SPIDER_NAME.value
    custom_settings = {
        'FEEDS': {
            GamePl.EXPORT_FILE_PATH.value: SPIDER_EXPORT
        },
        "FEED_EXPORT_ENCODING": "utf-8",
        'AUTOTHROTTLE_ENABLED': True
    }


    def __init__(self, *args, **kwargs):
        """
        Constructor that initializes the Spider instance and sets it up
        """
        super().__init__(*args, **kwargs)
        chrome_options = Options()  
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                       chrome_options = chrome_options)


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        This method connects the Spider with a termination signal in order to
        automatically execute operations when the Spider closes
        """
        spider = super(GamePlSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal = scrapy.signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        """
        Function that is called in the moment of Spider termination. The Spider
        calls it's Selenium driver quit method
        """
        self.driver.quit()


    def parse_product(self, response):
        """
        Retrieves product information from the product detail page, and exports
        it to the output json
        """
        self.log(f'>>>>> ATTEMPTING TO SCRAP {response.url}<<<<<')

        self.driver.implicitly_wait(2)

        self.driver.get(response.url)
        name_xp = f'//h1[@class="{GamePl.TITLE_CLASS.value}"]'
        name = self.driver.find_elements_by_xpath(name_xp)[0].get_attribute('innerText')

        desc_xp = f'//div[@class="{GamePl.DESC_CLASS.value}"]'
        description = self.driver.find_elements_by_xpath(desc_xp)[0].get_attribute('innerText')

        price_xp = f'//div[contains(@class, "{GamePl.PRICE_CLASS.value}")]//span'
        price = self.driver.find_elements_by_xpath(price_xp)[0].get_attribute('innerText')
        price = int(float(price.replace("$","").replace(",","").replace(".","")))

        image_xp = (f'//img[@id = "{GamePl.IMAGE_ID.value}"]')
        image_url = self.driver.find_elements_by_xpath(image_xp)[0].get_attribute('src')
        image = image_url

        tag_xp = (f'//span[@class = "{GamePl.TAG_CLASS.value}"]')
        tag_product = self.driver.find_elements_by_xpath(tag_xp)[0].get_attribute('innerText')
        if "switch" in tag_product.lower():
            id_type_product = 1
        if "xbox" in tag_product.lower():
            id_type_product = 2
        if "playstation" in tag_product.lower():
            id_type_product = 3
        
        barcode_xp = f'//input[@name="{GamePl.ID_CLASS.value}"]'
        barcode = self.driver.find_element_by_xpath(barcode_xp).get_attribute('value')
        barcode = validate_sku(barcode)

        yield {
            'name': name,
            'description': description,
            'id_ecommerce': SITE_IDS['GamePlanet'],
            'id_type_product': id_type_product,
            'price': price,
            'image': image,
            'url': response.url,
            'barcode': barcode
        }


    def parse(self, response):
        """
        Retrieves information for all products in terms of the fields: name,
        description, price, image, and url
        """
        self.driver.get(response.url)
        next_xp = (f'//a[@title = "Next"]')
        next_page = self.driver.find_elements_by_xpath(next_xp)
        if len(next_page) > 0:
            next_url = next_page[0].get_attribute('href')
            yield response.follow(next_url, callback = self.parse)

        product_xp = (f'//div[contains(@class, "{GamePl.ITEM_CLASS.value}")]/div[@class = "row"]/div/a')
        product_urls = self.driver.find_elements_by_xpath(product_xp)
        for url in product_urls:
            yield response.follow(url.get_attribute('href'), callback = self.parse_product)


class SearSpider(scrapy.Spider):
    """
    This Spider scraps products from the Sears e-commerce site
    """
    name = SEA.SPIDER_NAME.value
    custom_settings = {
        'FEEDS': {
            SEA.EXPORT_FILE_PATH.value: SPIDER_EXPORT
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

        name_xp = f'//div[@class = "{SEA.TITLE_CLASS.value}"]/h1/text()'
        name = response.xpath(name_xp).get()

        desc_xp = f'//div[@class = "{SEA.DESC_CLASS.value} yotpo-main-widget"]/@data-description'
        description = response.xpath(desc_xp)[0].get()

        price_xp = f'//p[@class = "{SEA.PRICE_CLASS.value}"]/text()'
        price = response.xpath(price_xp).get()
        price = int(float(price.replace("$","").replace(",","").replace(".","")))

        image_xp = (f'//ul[contains(@class,{SEA.IMAGE_CLASS.value})]/li/img/@src')
        image = response.urljoin(response.xpath(image_xp)[0].get())

        tag_xp = (f'//div[@class = "breadcrumb"]/ul/li[3]/a/text()')
        tag_product = response.xpath(tag_xp).get()

        if "nintendo" in tag_product.lower():
            id_type_product = 1
        if "xbox" in tag_product.lower():
            id_type_product = 2
        if "playstation" in tag_product.lower():
            id_type_product = 3

        barcode_xp = f'//script[{SEA.ID_PROP.value}]/@data-flix-ean'
        barcode_content = response.xpath(barcode_xp).get()
        barcode = validate_sku(barcode_content)

        yield {
            'name': name,
            'description': description,
            'id_ecommerce': SITE_IDS['Sears'],
            'id_type_product': id_type_product,
            'price': price,
            'image': image,
            'url': response.url,
            'barcode': barcode
        }


    def parse(self, response):
        """
        Retrieves information for all products in terms of the fields: name,
        description, price, image, and url
        """
        list_items = response.xpath('//div[contains(@class, "paginador")]/ul/li/a')
        page_buttons_xp = '//div[contains(@class, "paginador")]/ul/li/a/@href'
        page_buttons = response.xpath(page_buttons_xp).getall()

        if len(page_buttons) > 1:
            last_item_class = list_items[-1]
            if last_item_class.xpath('@class').get() != 'active':
                next_page = page_buttons[-1]
                yield response.follow(response.urljoin(next_page), callback = self.parse)

        product_xp = (f'//div[@class = "{SEA.ITEM_CLASS.value}"]/a[@class = "{SEA.LINK_CLASS.value}"]/@href')
        product_urls = response.xpath(product_xp).getall()

        for url in product_urls:
            yield response.follow(url, callback = self.parse_product)


class MixUpSpider(scrapy.Spider):
    """
    This Spider scraps products from the MixUp e-commerce site
    """
    name = MU.SPIDER_NAME.value
    custom_settings = {
        'FEEDS': {
            MU.EXPORT_FILE_PATH.value: SPIDER_EXPORT
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
        'AUTOTHROTTLE_ENABLED': True
    }


    def __init__(self, *args, **kwargs):
        """
        Constructor that initializes the Spider instance and sets it up
        """
        super().__init__(*args, **kwargs)
        chrome_options = Options()  
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                       chrome_options = chrome_options)


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        This method connects the Spider with a termination signal in order to
        automatically execute operations when the Spider closes
        """
        spider = super(MixUpSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal = scrapy.signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        """
        Function that is called in the moment of Spider termination. The Spider
        calls it's Selenium driver quit method
        """
        spider.driver.quit()


    def parse_product(self, response):
        """
        Retrieves product information from the product detail page, and exports
        it to the output json
        """
        self.log(f'\n>>>>> ATTEMPTING TO SCRAP {response.url}<<<<<\n')

        name_xp = f'//div[@class="{MU.TITLE_CLASS.value}"]/text()'
        name = response.xpath(name_xp).get().strip()

        desc_xp = f'//div[@class="{MU.DESC_CLASS.value}"]//div[@class = "texto"]/text()'
        description = response.xpath(desc_xp).get()
        description = description.strip()

        price_xp = f'//span[contains(@class, "{MU.PRICE_CLASS.value}")]/text()'
        price = response.xpath(price_xp)[1].get()
        price = price.strip()         
        price = int(float(price.replace("$", "").replace(",", "").replace(".", "")))

        image_xp = (f'//img[@id="{MU.IMAGE_ID.value}"]/@src')
        image = response.urljoin(response.xpath(image_xp).get())

        tag_xp = (f'//div[@id = "ctl00_container_PanelAutor"]/div[@class = "titulo"]/text()')
        tag_product = response.xpath(tag_xp).getall()
        tag_product = ''.join(tag_product)
        tag_product = tag_product.strip()

        if "switch" in tag_product.lower():
            id_type_product = 1
        if "xbox" in tag_product.lower():
            id_type_product = 2
        if "playstation" in tag_product.lower():
            id_type_product = 3
        
        barcode_xp = f'//input[@name="{MU.BARCODE_ID.value}"]/@value'
        barcode_content = response.xpath(barcode_xp).get()
        barcode = validate_sku(barcode_content)

        yield {
            'name': name,
            'description': description,
            'id_type_product': id_type_product,
            'id_ecommerce': SITE_IDS['MixUp'],
            'price': price,
            'image': image,
            'url': response.url,
            'barcode': barcode
        }


    def parse(self, response):
        """
        Retrieves information for all products in terms of the fields: name,
        description, price, image, and url
        """
        self.driver.get(response.url)
        
        product_urls = []
        product_xp = (f'//div[@class = "{MU.ITEM_CLASS_1.value}"]/div[@class = "{MU.ITEM_CLASS_2.value}"]/a')
        products = self.driver.find_elements_by_xpath(product_xp)

        for product in products:
            product_urls.append(product.get_attribute('href'))

        try:
            next_button = self.driver.find_elements_by_xpath('//a[@id = "ctl00_container_linkPnts2Up"]')
            next_button = next_button[0]
            next_button.click()
            condition = True
        except IndexError:
            condition = False
            pass

        while (condition):
            self.log(f'condition: {condition}')
            self.driver.implicitly_wait(2)
            new_products = self.driver.find_elements_by_xpath(product_xp)
            for product in new_products:
                new_url = product.get_attribute('href')
                product_urls.append(new_url)
            next_button = self.driver.find_elements_by_xpath('//a[@id = "ctl00_container_linkPnts2Up"]')
            next_button = next_button[0]
            disabled = next_button.get_attribute('disabled')
            condition = disabled != 'true'
            next_button.click()
            
        for url in product_urls:
            yield response.follow(url, callback = self.parse_product)
