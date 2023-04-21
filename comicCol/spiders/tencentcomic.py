import scrapy
from comicCol.items import ComicItem
from comicCol.items import ChapterItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TencentcomicSpider(scrapy.Spider):
    name = 'tencentcomic'
    allowed_domains = ["ac.qq.com"]
    base_url = 'https://ac.qq.com/Comic/index/page/{}'
    start_urls = ['https://ac.qq.com/Comic/']

    def start_requests(self):
        for page in range(1, 2):
            url = self.base_url.format(page)
            yield scrapy.Request(url, callback=self.parse)
        # yield SeleniumRequest(
        #     url=url,
        #     callback=self.parse,
        #     wait_time=10,
        #     wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'mod_page_next')),
        #     script="document.querySelector('.mod_page_next').click()"
        # )

    def parse(self, response):
        comics = response.css('li.ret-search-item')
        comic_item = ComicItem()
        comic_item['site'] = 'Tencent'
        comic_item['status'] = ''
        for comic in comics:
            comic_item['comicName'] = comic.css('a.mod-cover-list-thumb').attrib['title']
            comic_item['comicAuthor'] = comic.css('p.ret-works-author::text').get()
            comic_item['comicInfo'] = comic.css('p.ret-works-decs::text').get()
            comic_item['tags'] = comic.css('p.ret-works-tags span::text').getall()[0:2]
            comic_item['imgUrl'] = comic.css('a.mod-cover-list-thumb img').attrib['data-original']
            comic_item['comicUrl'] = "https://ac.qq.com{}".format(comic.css('div.ret-works-cover a').attrib['href'])
            yield comic_item
            yield SeleniumRequest(
                url=comic_item['comicUrl'],
                callback=self.parse_detail,
                # wait_time=10,
                # wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'mod_page_next')),
                # script="document.querySelector('.mod_page_next').click()"
            )

    # 解析漫画详情
    def parse_detail(self, response):
        chapter_item = ChapterItem()
        chapters = response.css('span.works-chapter-item')

        chapter_item['comicName'] = response.css('h2.works-intro-title strong::text').get()
        for chapter in chapters:
            chapter_item['chapterName'] = chapter.css('a::text').get().strip()
            chapter_item['chapterUrl'] = "https://ac.qq.com{}".format(chapter.css('a').attrib['href'])
            yield chapter_item

    def prase_chapter_all_image(self, response):
        pass
        # chapter_image_item = ChapterImageItem()
        # imageUrls = response.css