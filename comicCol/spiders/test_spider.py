from scrapy_selenium import SeleniumRequest

import scrapy
from selenium import webdriver


class TestSpiderSpider(scrapy.Spider):
    name = "test_spider"

    def start_requests(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(40)
        url = 'https://www.copymanga.site/comic/dianjuren/chapter/dc312a94-f526-11e8-a7d3-00163e0ca5bd'
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=400)

    def parse(self, response):
        yield {
            'urls': response.xpath('/html/body/div[2]/div/ul/li/img/@src').get()
        }
