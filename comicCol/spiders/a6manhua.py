import scrapy
from comicCol.items import ComicItem
from comicCol.items import ChapterItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
class A6manhuaSpider(scrapy.Spider):
    name = "6manhua"
    allowed_domains = ["6mh67.com"]
    base_url = "http://www.6mh67.com/rank/1-{}.html"

    def start_requests(self):
        for page in range(1, 2):
            url = self.base_url.format(page)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        comics = response.css('div.cy_list_mh ul')
        for i in range(len(comics)):
            url = "http://www.6mh67.com{}".format(comics[i].css('li.title a').attrib['href'])
            yield SeleniumRequest(
                url=url,
                callback=self.parse_detail,
                wait_time=10,
                wait_until=EC.element_located_to_be_selected((By.LINK_TEXT, '↓ 展开查看全部章节 ↓')),
                script="document.querySelector('#zhankai').click()"
            )

    def parse_detail(self, response):
        comic_item = ComicItem()
        comic_item['site'] = '6manhua'
        comic_item['comicName'] = str(response.css('div.cy_title h1::text').get())
        comic_item['comicAuthor'] = str(response.xpath('//*[@id="intro_l"]/div[3]/span[1]/text()').get()[3:])
        comic_item['comicInfo'] = str(response.xpath('//*[@id="comic-description"]/text()').get())
        comic_item['tags'] = str(response.xpath('//*[@id="intro_l"]/div[4]/span[2]/text()').get()[3:])
        comic_item['imgUrl'] = str(response.xpath('//*[@id="intro_l"]/div[1]/img/@src').get())
        comic_item['comicUrl'] = "http://www.6mh67.com/{}/".format(response.xpath('//*[@id="intro_l"]/div[6]/div[1]/a/@href').get().split("/")[1])
        comic_item['status'] = response.xpath('//*[@id="intro_l"]/div[3]/span[2]/font/text()').get()

        yield comic_item

        chapter_item = ChapterItem()
        chapters = response.css('div.cy_plist ul li')
        chapter_item['comicName'] = str(response.css('div.cy_title h1::text').get())
        for chapter in chapters:
            chapter_item['chapterName'] = chapter.css('a p::text').get()
            chapter_item['chapterUrl'] = "http://www.6mh67.com{}".format(chapter.css('a').attrib['href'])
            yield chapter_item