import scrapy
from comicCol.items import ComicItem
from comicCol.items import ChapterItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
class A6manhuaSpider(scrapy.Spider):
    name = "6manhua"
    allowed_domains = ["6mh67.com"]
    start_urls = ["http://www.6mh67.com/rank/1-1.html"]

    def parse(self, response):
        comics = response.css('div.cy_list_mh ul')
        comic_item = ComicItem()
        comic_item['site'] = '6manhua'
        for comic in comics:
            comic_item['comicName'] = comic.css('li.title a::text').get()
            comic_item['comicAuthor'] = ""
            comic_item['comicInfo'] = comic.css('li.info::text').get()
            comic_item['tags'] = comic.css('li.biaoqian::text').get()
            comic_item['imgUrl'] = comic.css('a.pic img').attrib['src']
            comic_item['comicUrl'] = "http://www.6mh67.com{}".format(comic.css('li.title a').attrib['href'])
            comic_item['status'] = comic.css('li.zuozhe::text').get()[3:]
            yield comic_item
            # yield scrapy.Request(url=comic_item['comicUrl'], callback=self.parse_detail)
            yield SeleniumRequest(
                url=comic_item['comicUrl'],
                callback=self.parse_detail,
                wait_time=10,
                wait_until=EC.element_to_be_clickable((By.ID, 'zhankai')),
                script="document.querySelector('#zhankai').click()"
            )

    def parse_detail(self, response):
        chapter_item = ChapterItem()
        chapters = response.css('div.cy_plist ul li')

        chapter_item['comicName'] = response.css('div.cy_title h1::text').get()
        for chapter in chapters:
            chapter_item['chapterName'] = chapter.css('p::text').get()
            chapter_item['chapterUrl'] = "http://www.6mh67.com{}".format(chapter.css('a').attrib['href'])
            yield chapter_item