import scrapy
import json
from comicCol.items import ComicItem
from comicCol.items import ChapterItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class CopycomicSpider(scrapy.Spider):
    name = "copycomic"
    allowed_domains = ["copymanga.site"]
    base_url = "https://www.copymanga.site/comics?ordering=-popular&offset={}&limit=50"

    def start_requests(self):
        for page in range(0, 1):
            url = self.base_url.format(page*50)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for comic in json.loads(response.css("div.exemptComic-box").attrib['list'].replace("'", "\"")):
            url = "https://www.copymanga.site/comic/{}".format(comic['path_word'])
            # yield scrapy.Request(url=url, callback=self.parse_detail(url=url))
            yield SeleniumRequest(
                url=url,
                callback=self.parse_detail,
                wait_time=10,
                wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'table-default')),
            )

    def parse_detail(self, response):
        comic_item = ComicItem()
        comic_item['comicName'] = str(response.css('h6::text').get())
        comic_item['comicAuthor'] = str(response.css('span.comicParticulars-right-txt a::text').getall())
        comic_item['comicInfo'] = str(response.css('p.intro::text').get())
        comic_item['tags'] = str(response.css('span.comicParticulars-tag a::text').getall())
        comic_item['imgUrl'] = str(response.css('div.comicParticulars-left-img img').attrib['data-src'])
        comic_item['comicUrl'] = "url"
        comic_item['site'] = 'copymanga'
        comic_item['status'] = str(response.xpath('/html/body/main/div[1]/div/div[2]/ul/li[6]/span[2]/text()').get())

        yield comic_item

        chapter_item = ChapterItem()
        chapter_item['comicName'] = response.css('h6::text').get()
        for chapter in response.css('div#default全部 ul a'):
            chapter_item['chapterName'] = str(chapter.css('li::text').get())
            chapter_item['chapterUrl'] = "https://www.copymanga.site{}".format(chapter.css('a').attrib['href'])
            yield chapter_item
